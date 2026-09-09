#!/usr/bin/env python3
"""HG PDLC 2.0: finite artifact checks, not a workflow runtime.

HG SDLC owns scheduling, attempts, retries, gates, artifact versions and audit.
This adapter uses the inspected .hgsdlc/nodes/<node>/attempt-N convention.
Run it from the HG project root. No network calls or model calls are made.
"""
from __future__ import annotations
import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
from typing import Any
import xml.etree.ElementTree as ET
import zipfile

VERSION = '2.0'
KINDS = {'INT','HYP','BR','AC','ADR','FR','NFR','CONTRACT','STORY','CODE','E2E','CHECK'}
INTENT = {'INT','HYP','BR','AC'}
DESIGN = KINDS - {'CODE'}
RELATIONS = {
 'motivates': ({'INT'}, {'HYP'}),
 'drives': ({'HYP'}, {'BR'}),
 'accepted_by': ({'BR'}, {'AC'}),
 'informs': ({'BR'}, {'ADR'}),
 'constrains': ({'ADR'}, {'FR','NFR','CONTRACT'}),
 'refined_by': ({'BR'}, {'FR','NFR'}),
 'specifies': ({'CONTRACT'}, {'FR'}),
 'planned_as': ({'FR','NFR'}, {'STORY'}),
 'implemented_by': ({'STORY'}, {'CODE'}),
 'tested_by': ({'AC'}, {'E2E'}),
 'verified_by': ({'FR','NFR'}, {'E2E','CHECK'}),
}
STAGE_FILES = {
 'prd': ['intent.md','hypothesis.md','PRD.md','decisions.json'],
 'design': ['intent.md','hypothesis.md','PRD.md','decisions.json','architecture.md',
            'architecture.dsl','adr.md','SRS.md','contracts.md','test-model.json','stories.json','epics.md'],
}
ID_RE = re.compile(r'^(?:INT|HYP|BR|AC|ADR|FR|NFR|CONTRACT|STORY|CODE|E2E|CHECK)-[A-Za-z0-9][A-Za-z0-9_.-]*$')
TEST_RE = re.compile(r'\[((?:E2E|CHECK)-[A-Za-z0-9][A-Za-z0-9_.-]*)\]')
SECRET_PARTS = {'.git','.hgsdlc','.pdlc','node_modules','__pycache__'}

class ContractError(RuntimeError):
    pass

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()

def canonical(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> Any:
    try:
        def unique(pairs):
            result={}
            for key,value in pairs:
                if key in result:raise ValueError('Duplicate JSON key: '+key)
                result[key]=value
            return result
        return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    except (OSError,ValueError) as exc:
        raise ContractError(f'Cannot read JSON: {path}: {exc}') from exc

def save(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    os.replace(temp,path)

def inside(root: Path, rel: str, *, dot: bool=False) -> Path:
    if not isinstance(rel,str) or not rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
        raise ContractError(f'Unsafe relative path: {rel!r}')
    if rel=='.' and not dot:
        raise ContractError('A file path cannot be dot')
    base=root.resolve(); p=base/rel
    for ancestor in [p,*p.parents]:
        if ancestor==base: break
        if ancestor.is_symlink(): raise ContractError(f'Symlink not allowed: {ancestor}')
    out=p.resolve()
    if out!=base and base not in out.parents: raise ContractError(f'Escaping root: {rel}')
    return out

def no_placeholders(value: Any) -> list[str]:
    text=json.dumps(value,ensure_ascii=False) if not isinstance(value,str) else value
    return ['Unresolved placeholder/TBD'] if re.search(r'\b(TBD|TODO|CHANGEME|PLACEHOLDER)\b|<change-id>|<название>|SHA256_',text) else []

def project_graph(g: dict, kinds: set[str]) -> dict:
    entities=[e for e in g.get('entities',[]) if e.get('kind') in kinds]
    ids={e['id'] for e in entities}
    return {'schema_version':g.get('schema_version'),'change_id':g.get('change_id'),
            'entities':sorted(entities,key=lambda x:x['id']),
            'links':sorted([l for l in g.get('links',[]) if l.get('from') in ids and l.get('to') in ids],
                           key=lambda x:(x['from'],x['to'],x['relation']))}

def graph_index(g: dict) -> tuple[dict,dict,dict]:
    entities={e['id']:e for e in g.get('entities',[])}
    before={i:set() for i in entities}; after={i:set() for i in entities}
    for link in g.get('links',[]):
        a,b=link.get('from'),link.get('to')
        if a in entities and b in entities: after[a].add(b); before[b].add(a)
    return entities,before,after

def closure(adjacency: dict, start: str) -> list[str]:
    result=set(); pending=list(adjacency.get(start,()))
    while pending:
        item=pending.pop()
        if item==start or item in result: continue
        result.add(item); pending.extend(adjacency.get(item,()))
    return sorted(result)

def impact(g: dict, entity_id: str) -> dict:
    entities,before,after=graph_index(g)
    if entity_id not in entities: raise ContractError('Unknown trace ID: '+entity_id)
    return {'entity_id':entity_id,'upstream':closure(before,entity_id),'downstream':closure(after,entity_id),
            'owner_stage':entities[entity_id]['owner_stage'],
            'note':'Graph impact, not an automatic root-cause diagnosis. A failed test does not authorize changing intent.'}

def validate_graph(g: Any, stage: str='ready') -> list[str]:
    errors=[]
    if not isinstance(g,dict): return ['Graph must be an object']
    if g.get('schema_version')!=VERSION: errors.append('Wrong graph schema_version')
    if not isinstance(g.get('change_id'),str) or not g['change_id']: errors.append('Missing change_id')
    if isinstance(g.get('entities'),list):
        all_ids=[]
        for entity in g['entities']:
            if not isinstance(entity,dict) or entity.get('kind') not in KINDS:
                errors.append('Unknown/malformed entity in graph')
            elif isinstance(entity.get('id'),str):all_ids.append(entity['id'])
        if len(set(all_ids))!=len(all_ids):errors.append('Duplicate global entity ID')
    # Later-stage remnants are deliberately stale after correct-course; validate them at their own gate.
    limits={'prd':INTENT,'architecture':INTENT|{'ADR','CONTRACT'},'srs':INTENT|{'ADR','CONTRACT','FR','NFR'},'ready':DESIGN}
    if stage in limits and isinstance(g.get('entities'),list) and isinstance(g.get('links'),list) and all(isinstance(e,dict) and 'id' in e for e in g['entities']):
        g=project_graph(g,limits[stage])
    raw=g.get('entities'); links=g.get('links')
    if not isinstance(raw,list) or not raw: return errors+['Nonempty entities required']
    if not isinstance(links,list): return errors+['links must be an array']
    entities={}
    for e in raw:
        if not isinstance(e,dict): errors.append('Entity must be object'); continue
        eid=e.get('id',''); kind=e.get('kind')
        if not isinstance(eid,str) or not ID_RE.fullmatch(eid): errors.append(f'Invalid ID: {eid}');continue
        if eid in entities: errors.append('Duplicate ID: '+eid)
        entities[eid]=e
        if kind not in KINDS or not eid.startswith(str(kind)+'-'): errors.append('ID/kind mismatch: '+eid)
        if type(e.get('revision')) is not int or e['revision']<1: errors.append('Invalid revision: '+eid)
        for field in ['title','owner_stage']:
            if not isinstance(e.get(field),str) or not e[field].strip(): errors.append(f'{eid}: missing {field}')
        if e.get('scope') not in ['in','out']: errors.append(eid+': scope must be in/out')
        origin=e.get('origin',{})
        if not isinstance(origin,dict):origin={}
        if not isinstance(origin,dict) or origin.get('kind') not in ['confirmed','observed','proposed','inferred']:
            errors.append(eid+': origin missing/invalid')
        else:
            if not isinstance(origin.get('sources'),list) or not origin['sources']: errors.append(eid+': origin sources required')
            for src in origin.get('sources',[]):
                if not isinstance(src,dict) or not src.get('reference') or not src.get('revision'):
                    errors.append(eid+': source needs reference and revision')
        art=e.get('artifact',{})
        if not isinstance(art,dict) or not all(isinstance(art.get(k),str) and art[k] for k in ['repo','path','anchor']):
            errors.append(eid+': artifact requires repo/path/anchor')
        if kind in INTENT and e.get('scope')=='in' and origin.get('kind') in ['observed','inferred']:
            errors.append(eid+': observed code/inference is not confirmed feature intent')
        if kind=='NFR' and e.get('verification_method') not in ['e2e','performance','security','static','inspection']:
            errors.append(eid+': NFR verification_method required')
    before={i:set() for i in entities}; after={i:set() for i in entities}; triples=set()
    for l in links:
        if not isinstance(l,dict): errors.append('Link must be object'); continue
        a,b,rel=l.get('from'),l.get('to'),l.get('relation')
        if a not in entities or b not in entities: errors.append(f'Dangling link: {a}->{b}'); continue
        triple=(a,b,rel)
        if triple in triples: errors.append(f'Duplicate link: {triple}')
        triples.add(triple)
        if a==b: errors.append('Self-link: '+a)
        if rel not in RELATIONS or entities[a]['kind'] not in RELATIONS[rel][0] or entities[b]['kind'] not in RELATIONS[rel][1]:
            errors.append(f'Illegal relation: {a} {rel} {b}')
        if l.get('from_revision')!=entities[a].get('revision') or l.get('to_revision')!=entities[b].get('revision'):
            errors.append(f'Stale revision link: {a}->{b}')
        before[b].add(a); after[a].add(b)
        if entities[a].get('scope')=='out' and entities[b].get('scope')=='in':
            errors.append(f'Out-of-scope ancestor used: {a}->{b}')
    active={i:e for i,e in entities.items() if e.get('scope')=='in'}
    def incoming(eid,kind): return any(entities[x]['kind'] in kind for x in before[eid])
    def outgoing(eid,kind): return any(entities[x]['kind'] in kind and entities[x].get('scope')=='in' for x in after[eid])
    required={'INT','HYP','BR','AC'}
    if stage in ['architecture','srs','ready','implemented','verified']: required|={'ADR'}
    if stage in ['srs','ready','implemented','verified']: required|={'FR'}
    if stage in ['ready','implemented','verified']: required|={'STORY','E2E'}
    if stage in ['implemented','verified']: required|={'CODE'}
    missing=required-{e['kind'] for e in active.values()}
    if missing: errors.append('Missing entity kinds: '+','.join(sorted(missing)))
    parents={'HYP':{'INT'},'BR':{'HYP'},'AC':{'BR'},'ADR':{'BR'},'FR':{'BR'},'NFR':{'BR'},
             'CONTRACT':{'ADR'},'STORY':{'FR','NFR'},'CODE':{'STORY'},'E2E':{'AC','FR'},'CHECK':{'NFR'}}
    for eid,e in active.items():
        kind=e['kind']
        if kind in parents and not incoming(eid,parents[kind]): errors.append('Orphan '+kind+': '+eid)
        if kind in ['FR','NFR'] and not incoming(eid,{'ADR'}): errors.append(eid+': no architecture decision')
        if kind=='E2E' and (not incoming(eid,{'AC'}) or not incoming(eid,{'FR','NFR'})):
            errors.append(eid+': E2E must link acceptance and system requirement')
        if kind=='INT' and not outgoing(eid,{'HYP'}): errors.append(eid+': no hypothesis')
        if kind=='HYP' and not outgoing(eid,{'BR'}): errors.append(eid+': no business requirements')
        if kind=='BR' and not outgoing(eid,{'AC'}): errors.append(eid+': no acceptance criterion')
        if stage in ['ready','implemented','verified']:
            if kind=='BR' and not outgoing(eid,{'FR','NFR'}): errors.append(eid+': no system refinement')
            if kind=='ADR' and not outgoing(eid,{'FR','NFR','CONTRACT'}): errors.append(eid+': unused ADR')
            if kind=='AC' and not outgoing(eid,{'E2E'}): errors.append(eid+': no E2E coverage')
            if kind=='FR' and not outgoing(eid,{'E2E'}): errors.append(eid+': no E2E coverage')
            if kind=='NFR' and not outgoing(eid,{'E2E','CHECK'}): errors.append(eid+': no verification coverage')
            if kind in ['FR','NFR'] and not outgoing(eid,{'STORY'}): errors.append(eid+': no implementation story')
        if stage in ['implemented','verified'] and kind=='STORY' and not outgoing(eid,{'CODE'}):
            errors.append(eid+': no implementation mapping')
    visited=set(); stack=set()
    def visit(i):
        if i in stack: errors.append('Trace cycle at '+i); return
        if i in visited:return
        stack.add(i)
        for j in after[i]:visit(j)
        stack.remove(i);visited.add(i)
    for i in entities:visit(i)
    return errors

def validate_model(model: dict, g: dict) -> list[str]:
    errors=[]; entities,before,_=graph_index(g); tests=model.get('tests',[])
    expected={i for i,e in entities.items() if e['kind'] in ['E2E','CHECK'] and e['scope']=='in'}
    ids=[t.get('id') for t in tests]
    if len(set(ids))!=len(ids): errors.append('Duplicate test-model ID')
    if set(ids)!=expected: errors.append('Test-model/graph ID set differs')
    if model.get('boundary') not in ['browser','api','cli']: errors.append('Explicit E2E boundary required')
    for t in tests:
        tid=t.get('id'); ent=entities.get(tid,{})
        if t.get('kind') not in ['e2e','check']:errors.append(f'{tid}: unknown test kind')
        if t.get('kind')=='e2e' and ent.get('kind')!='E2E':errors.append(f'{tid}: kind differs')
        if t.get('mandatory') is not True:errors.append(f'{tid}: in-scope checks cannot be optional')
        for k in ['given','when']:
            if not isinstance(t.get(k),str) or not t[k].strip():errors.append(f'{tid}: missing {k}')
        if not isinstance(t.get('then'),list) or not t['then'] or not all(isinstance(x,str) and x.strip() for x in t['then']):
            errors.append(f'{tid}: observable assertions required')
        ancestors=before.get(tid,set())
        req={i for i in ancestors if entities[i]['kind'] in ['FR','NFR']}
        ac={i for i in ancestors if entities[i]['kind']=='AC'}
        if t.get('kind')=='check' and ent.get('kind')!='CHECK':errors.append(f'{tid}: kind differs')
        if set(t.get('requirements',[]))!=req or set(t.get('acceptance',[]))!=ac:
            errors.append(f'{tid}: model references differ from trace graph')
    return errors+no_placeholders(model)

def parse_junit(path: Path, required: set[str]) -> tuple[dict,list[str]]:
    """Strict on missing/duplicate IDs, skips, failures, xfail and suite errors."""
    errors=[]; results={}
    try:
        text=path.read_text(encoding='utf-8')
        if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper(): raise ValueError('DTD not allowed')
        root=ET.fromstring(text)
    except (OSError,ET.ParseError,ValueError) as exc:
        return {},[f'Invalid/missing JUnit: {exc}']
    if root.tag not in ['testsuites','testsuite']: errors.append('Unexpected JUnit root')
    cases=list(root.iter('testcase'))
    if not cases: errors.append('Empty JUnit suite')
    for suite in root.iter('testsuite'):
        for field in ['errors','failures']:
            try:
                if float(suite.get(field,'0'))>0: errors.append('Suite '+field+' > 0')
            except ValueError: errors.append('Non-numeric suite result')
    for case in cases:
        title=case.get('name','')
        ids=TEST_RE.findall(title)
        if len(ids)!=1: errors.append('One [TEST-ID] required in testcase name: '+title);continue
        tid=ids[0]
        status='passed'
        if case.find('failure') is not None or case.find('error') is not None: status='failed'
        elif case.find('skipped') is not None: status='skipped'
        if tid in results: errors.append('Duplicate/retried testcase ID: '+tid)
        if tid not in required: errors.append('Unknown/unplanned testcase ID: '+tid)
        results[tid]={'status':status,'name':title,'classname':case.get('classname',''),'duration':case.get('time','0')}
        if status!='passed': errors.append(tid+': '+status)
    for tid in sorted(required-set(results)): errors.append('Missing testcase: '+tid)
    return results,errors

class Native:
    """Thin adapter to native HG paths. No independent run-state files."""
    def __init__(self, root: Path, node: str):
        self.root=root.resolve()
        if not re.fullmatch(r'[a-z0-9-]+',node):raise ContractError('Invalid node id')
        self.node=node
        self.native=self.root/'.hgsdlc'/'nodes'
        # Runtime creates the current node's attempt directory before launching a command.
        attempts=self.attempts(node)
        if not attempts:raise ContractError('HG attempt directory missing; this is not a standalone orchestrator')
        self.attempt,self.out=attempts[-1]
        matches=list((self.native/'ai-intake').glob('attempt-*/binding.json'))
        if len(matches)!=1:raise ContractError('Exactly one immutable ai-intake binding required; no guessing latest')
        self.binding=load(matches[0])
        if self.binding.get('schema_version')!=VERSION:raise ContractError('Binding version mismatch')
        self.change=inside(self.root,self.binding['change_dir'])
        if not re.fullmatch(r'pdlc/changes/[A-Za-z0-9][A-Za-z0-9_-]*',self.binding['change_dir']):
            raise ContractError('Change must be under pdlc/changes/<id>')
        if self.change.name!=self.binding['change_id']:raise ContractError('Binding/change mismatch')
        self.run_id=self.binding['run_id']
    def attempts(self,node):
        base=self.native/node
        result=[]
        for p in base.glob('attempt-*'):
            if p.is_symlink():raise ContractError('Native artifact symlink rejected')
            m=re.fullmatch(r'attempt-(\d+)',p.name)
            if m and p.is_dir():result.append((int(m.group(1)),p))
        return sorted(result)
    def source(self,node,file,required=True):
        attempts=self.attempts(node)
        if not attempts:
            if required:raise ContractError('Missing predecessor artifact: '+node+'/'+file)
            return None
        # Mandatory artifact_ref in FLOW establishes successful predecessor execution.
        # Refuse missing file in newest attempt instead of silently taking an old pass.
        p=inside(attempts[-1][1],file)
        if not p.is_file():
            if required:raise ContractError('Missing current predecessor artifact: '+str(p))
            return None
        return p
    def graph(self):
        graph=load(self.change/'trace/graph.json')
        if graph.get('change_id')!=self.binding['change_id']:
            raise ContractError('Trace graph belongs to another change')
        return graph
    def registry(self):
        data=load(self.root/'pdlc/product/repositories.json')
        repos=data.get('repositories',[])
        ids=[r.get('id') for r in repos]
        if not repos or len(ids)!=len(set(ids)):raise ContractError('Empty/duplicate repository registry')
        if data.get('docs_repo') not in ids:raise ContractError('docs_repo missing from registry')
        for r in repos:
            inside(self.root,r['path'],dot=True)
            if not r.get('source_globs'):raise ContractError('Source coverage globs required for every repository')
        return data
    def snapshot(self):
        """Actual bytes + Git heads for declared source coverage, including untracked source."""
        reg=self.registry(); result={}
        for r in reg['repositories']:
            root=inside(self.root,r['path'],dot=True)
            if not root.is_dir():raise ContractError('Repository unavailable: '+r['id'])
            files={}
            candidates=set()
            for glob in r['source_globs']:
                if '..' in Path(glob).parts or Path(glob).is_absolute():raise ContractError('Unsafe source glob')
                candidates.update(root.glob(glob+'/*' if glob.endswith('/**') else glob))
            for p in sorted(candidates):
                if p.is_symlink():raise ContractError('Source symlink rejected: '+str(p))
                if not p.is_file():continue
                rel=p.relative_to(root).as_posix()
                if any(part in SECRET_PARTS or part=='pdlc' for part in p.relative_to(root).parts):continue
                if p.name.startswith('.env') or p.suffix.lower() in ['.pem','.key','.p12']:continue
                if any(fnmatch.fnmatch(rel,x) for x in r.get('exclude_globs',[])):continue
                inside(root,rel)
                files[rel]=digest(p)
            head='NO_GIT'
            try:
                c=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,timeout=10)
                if c.returncode==0:head=c.stdout.strip()
            except (OSError,subprocess.TimeoutExpired):pass
            result[r['id']]={'path':r['path'],'head':head,'files':files}
        return {'repositories':result,'registry_digest':canonical(reg)}
    def coord(self,path):
        p=path.resolve()
        rel=p.relative_to(self.native)
        parts=rel.parts
        return {'run_id':self.run_id,'node_id':parts[0],'attempt':int(parts[1].split('-')[1]),
                'path':'/'.join(parts[2:]),'sha256':digest(p)}
    def subject(self,kind):
        g=self.graph()
        if kind in ['prd','design']:
            files={f:digest(self.change/f) for f in STAGE_FILES[kind]}
            if kind=='design':
                feature=self.change/'test-model.feature'
                if feature.is_file():files['test-model.feature']=digest(feature)
                contracts=self.change/'contracts'
                if contracts.is_dir():
                    for p in sorted(contracts.rglob('*')):
                        if p.is_file():
                            safe=inside(self.change,p.relative_to(self.change).as_posix());files[p.relative_to(self.change).as_posix()]=digest(safe)
            kinds=INTENT if kind=='prd' else DESIGN
            extra={}
            if kind=='design':
                extra={f:digest(self.root/'pdlc/product'/f) for f in ['repositories.json','verification.json']}
            return canonical({'files':files,'graph':project_graph(g,kinds),'profiles':extra})
        if kind=='code':
            return canonical({'source':self.snapshot(),'graph':g,'map':load(self.change/'implementation-map.json')})
        if kind=='acceptance':
            evidence=load(self.source('command-e2e','evidence.json'))
            return canonical({'code':self.subject('code'),'evidence':evidence,
                              'checks':load(self.source('command-checks','checks-evidence.json'))})
        raise ContractError('Unknown subject kind')
    def check_freeze(self,phase):
        source='command-freeze-intent' if phase=='prd' else 'command-freeze-design'
        frozen=load(self.source(source,'freeze.json'))
        if frozen.get('subject_digest')!=self.subject(phase):raise ContractError('Frozen '+phase+' changed; return through its author and approval/readiness')
    def artifact_paths(self,kinds=None):
        registry=self.registry(); repos={r['id']:inside(self.root,r['path'],dot=True) for r in registry['repositories']}
        errors=[]
        for entity in self.graph()['entities']:
            if entity['scope']!='in' or (kinds is not None and entity['kind'] not in kinds):continue
            a=entity['artifact']
            if a['repo'] not in repos:errors.append('Unknown repo for '+entity['id']);continue
            p=inside(repos[a['repo']],a['path'])
            if not p.is_file():
                # Deleted CODE paths are tombstones backed by the native initial inventory.
                mapping=load(self.change/'implementation-map.json') if entity['kind']=='CODE' and (self.change/'implementation-map.json').is_file() else {}
                tombstone=next((x for x in mapping.get('items',[]) if x.get('id')==entity['id'] and x.get('action')=='delete' and x.get('repo')==a['repo'] and x.get('path')==a['path']),None)
                if tombstone:
                    inventory=load(self.source('command-inventory','inventory.json'))
                    previous=inventory.get('source_snapshot',{}).get('repositories',{}).get(a['repo'],{}).get('files',{})
                    if a['path'] in previous:continue
                errors.append('Missing artifact for '+entity['id']);continue
            if p.stat().st_size>5_000_000:errors.append('Text artifact too large for anchor validation');continue
            try:text=p.read_text(encoding='utf-8')
            except UnicodeError:errors.append('Non-text trace artifact');continue
            if a['anchor'] not in text:errors.append('Missing anchor for '+entity['id'])
        return errors
    def review(self,node,role,subject,expected_ids):
        data=load(self.source(node,'review.json')); errors=[]
        if data.get('role')!=role:errors.append('Wrong review role: '+node)
        if data.get('verdict')!='pass':errors.append('Review not pass: '+node)
        if data.get('subject_digest')!=self.subject(subject):errors.append('Stale review: '+node)
        if not expected_ids<=set(data.get('checked_ids',[])):errors.append('Review did not cover all required IDs: '+node)
        if any(f.get('severity') in ['blocking','critical','high'] for f in data.get('findings',[])):
            errors.append('Blocking review finding: '+node)
        return errors
    def summary(self,route,errors,extra=None):
        report={'schema_version':VERSION,'verdict':'pass' if not errors else 'blocked','errors':errors,
                'run_id':self.run_id,'node_id':self.node,'attempt':self.attempt,'created_at':now(),**(extra or {})}
        save(self.out/'report.json',report)
        summary={'step_id':self.node,'attempt':self.attempt,'status':'done','route':route,
                 'actions':['Artifact checks completed; verdict='+report['verdict']],
                 'rework_instruction':'\n'.join(errors) if errors else '', 'report':self.coord(self.out/'report.json')}
        save(self.out/'step-summary.json',summary)
        print('STEP_SUMMARY:\n```json\n'+json.dumps(summary,ensure_ascii=False)+'\n```')


def ids_of(g,kinds):return {e['id'] for e in g['entities'] if e['kind'] in kinds and e['scope']=='in'}

def check_stories(w: Native):
    g=w.graph(); data=load(w.change/'stories.json'); stories=data.get('stories',[]); errors=[]
    ids=[s.get('id') for s in stories]
    if len(set(ids))!=len(ids) or set(ids)!=ids_of(g,{'STORY'}):errors.append('Stories/graph differ or duplicate IDs')
    index={s['id']:s for s in stories}; entities,before,_=graph_index(g)
    deps={s['id']:set(s.get('depends_on',[])) for s in stories}
    for s in stories:
        sid=s['id']
        if any(d not in index or d==sid for d in deps[sid]):errors.append(sid+': invalid dependencies')
        if sid in closure(deps,sid):errors.append(sid+': cycle')
        if not s.get('tasks') or not s.get('definition_of_done'):errors.append(sid+': incomplete story')
        actual={i for i in before.get(sid,[]) if entities[i]['kind'] in {'FR','NFR'}}
        if set(s.get('requirements',[]))!=actual:errors.append(sid+': requirement references differ')
        if not set(s.get('acceptance',[]))<=ids_of(g,{'AC'}):errors.append(sid+': unknown AC')
    seen=set();active=set()
    def visit(i):
        if i in active:errors.append('Story dependency cycle');return
        if i in seen or i not in deps:return
        active.add(i)
        for j in deps[i]:visit(j)
        active.remove(i);seen.add(i)
    for i in deps:visit(i)
    return errors+no_placeholders(data)

def profile(w: Native):
    p=load(w.root/'pdlc/product/verification.json')
    if p.get('configured') is not True:raise ContractError('Product verification profile not configured')
    if p.get('boundary',{}).get('kind') not in ['browser','api','cli']:raise ContractError('Verification boundary missing')
    for key in ['checks','e2e']:
        c=p.get(key,{})
        if not isinstance(c.get('argv'),list) or not c['argv'] or not all(isinstance(x,str) and x for x in c['argv']):
            raise ContractError('Finite argv command required for '+key)
        inside(w.root,c.get('cwd','.'),dot=True)
        if type(c.get('timeout_seconds')) is not int or not 1<=c['timeout_seconds']<=3600:
            raise ContractError('Command timeout must be 1..3600 seconds')
    return p

def validate_implementation(w: Native):
    data=load(w.change/'implementation-map.json'); g=w.graph();errors=[]
    reg=w.registry(); repos={r['id']:inside(w.root,r['path'],dot=True) for r in reg['repositories']}
    items=data.get('items',[]); ids=[x.get('id') for x in items]
    if len(set(ids))!=len(ids) or set(ids)!=ids_of(g,{'CODE'}):errors.append('CODE IDs differ from implementation-map')
    entities,before,_=graph_index(g)
    snapshot=w.snapshot()
    initial=load(w.source('command-inventory','inventory.json')).get('source_snapshot',{}).get('repositories',{})
    for item in items:
        if item.get('repo') not in repos:errors.append('Unknown implementation repo');continue
        p=inside(repos[item['repo']],item['path'])
        if item.get('action')=='delete':
            if p.exists():errors.append('Deleted implementation still exists: '+item['path'])
            inventory=load(w.source('command-inventory','inventory.json'))
            previous=inventory.get('source_snapshot',{}).get('repositories',{}).get(item['repo'],{}).get('files',{})
            if item['path'] not in previous:errors.append('Deletion lacks initial source inventory: '+item['path'])
        else:
            if item.get('action') not in ['create','modify']:errors.append('Unknown implementation action')
            if not p.is_file():errors.append('Implementation file missing: '+item['path'])
            if item['path'] not in snapshot['repositories'][item['repo']]['files']:
                errors.append('Implementation file outside snapshot source coverage: '+item['path'])
            previous=initial.get(item['repo'],{}).get('files',{})
            if item.get('action')=='create' and item['path'] in previous:errors.append('Created file existed in initial inventory')
            if item.get('action')=='modify':
                if item['path'] not in previous:errors.append('Modified file missing from initial inventory')
                elif p.is_file() and digest(p)==previous[item['path']]:errors.append('Declared modification has no byte change')
        entity=entities.get(item.get('id'),{})
        if entity.get('artifact',{}).get('repo')!=item['repo'] or entity.get('artifact',{}).get('path')!=item['path']:
            errors.append('Implementation-map/trace location mismatch')
        if item.get('story') not in before.get(item.get('id'),set()):errors.append('CODE/story mismatch')
    bindings=data.get('test_bindings',[]);tids=[x.get('test_id') for x in bindings]
    if len(set(tids))!=len(tids) or set(tids)!=ids_of(g,{'E2E','CHECK'}):errors.append('All test IDs require exactly one executable binding')
    for b in bindings:
        if b.get('repo') not in repos:errors.append('Unknown test repo');continue
        p=inside(repos[b['repo']],b['path'])
        if not p.is_file():errors.append('Executable test file missing');continue
        if b['path'] not in snapshot['repositories'][b['repo']]['files']:errors.append('Test outside snapshot coverage')
        if '['+b['test_id']+']' not in p.read_text(encoding='utf-8'):errors.append('Test ID absent in executable source: '+b['test_id'])
    return errors+no_placeholders(data)

def gate(w: Native,stage: str,controlled=False):
    errors=[];g=w.graph()
    if stage=='prd':
        errors+=validate_graph(g,'prd')+w.artifact_paths(INTENT)
        for f in STAGE_FILES['prd']:errors+=no_placeholders((w.change/f).read_text(encoding='utf-8'))
        errors+=w.review('ai-prd-review','pdlc-prd-reviewer','prd',ids_of(g,INTENT))
        decisions=load(w.change/'decisions.json')
        if decisions.get('unresolved_blocking'):errors.append('Blocking intent questions remain')
        route='on_rework' if errors else 'on_success'
    elif stage=='ready':
        w.check_freeze('prd');errors+=validate_graph(g,'ready')+w.artifact_paths(DESIGN)
        errors+=validate_model(load(w.change/'test-model.json'),g)+check_stories(w)
        for f in STAGE_FILES['design']:errors+=no_placeholders((w.change/f).read_text(encoding='utf-8'))
        p=profile(w)
        if p['boundary']['kind']!=load(w.change/'test-model.json')['boundary']:errors.append('Test model/profile boundary differs')
        errors+=w.review('ai-design-review','pdlc-design-reviewer','design',ids_of(g,DESIGN))
        declared_risk=load(w.change/'decisions.json').get('risk_level','unknown')
        review_risk=load(w.source('ai-design-review','review.json')).get('risk_level','unknown')
        order={'low':0,'medium':1,'high':2,'unknown':3}
        risk=max([declared_risk,review_risk],key=lambda r:order.get(r,3))
        if risk not in ['low','medium','high','unknown']:errors.append('Unknown risk classification')
        route='on_rework' if errors else ('on_risk' if controlled or risk!='low' else 'on_success')
    elif stage=='code':
        w.check_freeze('prd');w.check_freeze('design')
        errors+=validate_graph(g,'implemented')+w.artifact_paths()+validate_implementation(w)
        errors+=w.review('ai-code-review','pdlc-code-reviewer','code',ids_of(g,{'CODE'}))
        errors+=w.review('ai-test-review','pdlc-test-reviewer','code',ids_of(g,{'E2E','CHECK'}))
        route='on_rework' if errors else 'on_success'
    elif stage in ['verify','final']:
        w.check_freeze('prd');w.check_freeze('design')
        errors+=validate_graph(g,'verified')+w.artifact_paths()+validate_implementation(w)
        errors+=validate_evidence(w)
        if stage=='final':errors+=w.review('ai-acceptance','pdlc-acceptance-auditor','acceptance',ids_of(g,{'AC','E2E','CHECK'}))
        route='on_rework' if errors else 'on_success'
        if not errors and stage=='verify':
            save(w.out/'trace-result.json',trace_result(w))
        if not errors and stage=='final':
            summary=trace_result(w)
            summary.update({'status':'verified-not-integrated','business_effect':'not-measured','code_snapshot':w.snapshot()})
            save(w.change/'validation-summary.json',summary)
            write_matrix(w.change/'trace/matrix.md',g,summary)
    else:raise ContractError('Unknown gate')
    w.summary(route,errors)
    return not errors

def execute_command(w: Native,kind: str):
    p=profile(w); cfg=p[kind]
    env=os.environ.copy();env['PDLC_EVIDENCE_DIR']=str(w.out);env['PDLC_RUN_ID']=w.run_id
    env['PDLC_CHANGE_ID']=w.binding['change_id'];env['PYTHONDONTWRITEBYTECODE']='1'
    stdout=w.out/'test.stdout.log'; stderr=w.out/'test.stderr.log'
    target=w.out/'junit.xml'
    # Reject accidental rerun inside the same native attempt instead of reusing files.
    if target.exists() or (w.out/'execution.json').exists():raise ContractError('Native attempt already has test outputs; request a new HG attempt')
    begun=now();start=time.monotonic();code=None;timed_out=False
    with stdout.open('w',encoding='utf-8') as out,stderr.open('w',encoding='utf-8') as err:
        try:
            process=subprocess.Popen(cfg['argv'],cwd=inside(w.root,cfg['cwd'],dot=True),env=env,
                                     stdout=out,stderr=err,start_new_session=True)
            try:code=process.wait(timeout=cfg['timeout_seconds'])
            except subprocess.TimeoutExpired:
                timed_out=True;os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
                code=124
        except OSError as exc:
            err.write(str(exc));code=127
    execution={'argv':cfg['argv'],'cwd':cfg['cwd'],'started_at':begun,'finished_at':now(),
               'duration_seconds':round(time.monotonic()-start,3),'exit_code':code,'timed_out':timed_out}
    save(w.out/'execution.json',execution)
    return execution

def run_tests(w: Native,kind: str):
    w.check_freeze('prd');w.check_freeze('design')
    if kind=='checks':
        errors=validate_graph(w.graph(),'implemented')+validate_implementation(w)
        errors+=w.review('ai-code-review','pdlc-code-reviewer','code',ids_of(w.graph(),{'CODE'}))
        errors+=w.review('ai-test-review','pdlc-test-reviewer','code',ids_of(w.graph(),{'E2E','CHECK'}))
        if errors:raise ContractError('\n'.join(errors))
    else:
        prior=load(w.source('command-checks','checks-evidence.json'))
        if prior.get('verdict')!='pass' or prior.get('source_digest')!=canonical(w.snapshot()) or prior.get('graph_digest')!=canonical(w.graph()) or prior.get('implementation_digest')!=canonical(load(w.change/'implementation-map.json')):
            raise ContractError('Checks are failed/stale; E2E cannot bypass them')
    source=w.snapshot();graph=w.graph();graph_hash=canonical(graph)
    execution=execute_command(w,kind); errors=[]
    required=ids_of(graph,{'E2E'} if kind=='e2e' else {'CHECK'})
    results={}
    if required or (w.out/'junit.xml').exists():results,errors=parse_junit(w.out/'junit.xml',required)
    if kind=='e2e' and not required:errors.append('No mandatory E2E tests')
    if execution['exit_code']!=0:errors.append('Actual process exit code: '+str(execution['exit_code']))
    if canonical(source)!=canonical(w.snapshot()):errors.append('Source changed during test execution')
    if graph_hash!=canonical(w.graph()):errors.append('Trace graph changed during test execution')
    artifacts=[]
    for f in ['junit.xml','test.stdout.log','test.stderr.log','execution.json']:
        if (w.out/f).exists():artifacts.append(w.coord(w.out/f))
    traces=w.out/'browser-traces'
    if traces.is_dir():
        with zipfile.ZipFile(w.out/'browser-traces.zip','w',zipfile.ZIP_DEFLATED) as z:
            for f in sorted(traces.rglob('*')):
                if f.is_symlink():raise ContractError('Trace symlinks rejected')
                if f.is_file():z.write(f,f.relative_to(traces))
        artifacts.append(w.coord(w.out/'browser-traces.zip'))
    evidence={'schema_version':VERSION,'kind':kind,'verdict':'pass' if not errors else 'blocked','errors':errors,
              'run_id':w.run_id,'node_id':w.node,'attempt':w.attempt,'graph_digest':graph_hash,
              'source_digest':canonical(source),'source_snapshot':source,'implementation_digest':canonical(load(w.change/'implementation-map.json')),'execution':execution,
              'boundary':profile(w)['boundary'],'results':results,'artifacts':artifacts}
    filename='evidence.json' if kind=='e2e' else 'checks-evidence.json'
    save(w.out/filename,evidence);save(w.out/'evidence-index.json',{'artifacts':[w.coord(w.out/filename),*artifacts]})
    w.summary('on_rework' if errors else 'on_success',errors,{'failed_ids':[i for i,v in results.items() if v['status']!='passed']})
    return not errors

def validate_evidence(w: Native):
    errors=[];current=canonical(w.snapshot()); graph=canonical(w.graph());all_results={}
    for node,file,kind in [('command-checks','checks-evidence.json','checks'),('command-e2e','evidence.json','e2e')]:
        source_path=w.source(node,file)
        data=load(source_path)
        if data.get('attempt')!=w.coord(source_path)['attempt']:errors.append('Evidence attempt mismatch')
        if data.get('kind')!=kind or data.get('run_id')!=w.run_id or data.get('node_id')!=node:errors.append('Evidence provenance mismatch')
        if data.get('verdict')!='pass':errors.append('Evidence is not pass: '+node)
        if data.get('source_digest')!=current:errors.append('Stale source evidence: '+node)
        if data.get('graph_digest')!=graph:errors.append('Stale graph evidence: '+node)
        if data.get('implementation_digest')!=canonical(load(w.change/'implementation-map.json')):errors.append('Stale implementation-map evidence: '+node)
        if data.get('execution',{}).get('exit_code')!=0:errors.append('Nonzero test exit')
        expected=ids_of(w.graph(),{'E2E'} if kind=='e2e' else {'CHECK'})
        if set(data.get('results',{}))!=expected:errors.append('Evidence result IDs differ from graph')
        for tid,r in data.get('results',{}).items():
            if r.get('status')!='passed':errors.append('Nonpassing mandatory test: '+tid)
            if tid in all_results:errors.append('Duplicate evidence test ID')
            all_results[tid]=r
        artifacts=data.get('artifacts',[])
        raw_required={'execution.json'}|({'junit.xml'} if expected else set())
        if not raw_required<={a.get('path') for a in artifacts}:errors.append('Missing required raw evidence declarations')
        for a in artifacts:
            if a.get('node_id')!=node or a.get('attempt')!=data.get('attempt'):errors.append('Cross-attempt evidence artifact')
            if a.get('run_id')!=w.run_id:errors.append('Cross-run artifact used');continue
            rel=f"{a['node_id']}/attempt-{a['attempt']}/{a['path']}"
            path=inside(w.native,rel)
            if not path.is_file() or digest(path)!=a.get('sha256'):errors.append('Missing/changed raw evidence artifact: '+rel)
            if a.get('path')=='junit.xml' and path.is_file():
                raw_results,raw_errors=parse_junit(path,expected)
                errors.extend(raw_errors)
                if raw_results!=data.get('results'):errors.append('Normalized results differ from raw JUnit')
            if a.get('path')=='execution.json' and path.is_file():
                if load(path)!=data.get('execution'):errors.append('Execution receipt differs from raw report')
    return errors

def trace_result(w: Native):
    g=w.graph();entities,before,after=graph_index(g);rows=[]
    results={};coords=[]
    for node,file in [('command-checks','checks-evidence.json'),('command-e2e','evidence.json')]:
        p=w.source(node,file);data=load(p);results.update(data['results']);coords.append(w.coord(p))
    for tid in sorted(ids_of(g,{'E2E','CHECK'})):
        up=closure(before,tid)
        rows.append({'test_id':tid,'status':results.get(tid,{}).get('status','missing'),
                     'upstream':up,'upstream_by_kind':{k:[i for i in up if entities[i]['kind']==k] for k in ['INT','HYP','BR','ADR','FR','NFR','AC']}})
    return {'schema_version':VERSION,'change_id':g['change_id'],'graph_digest':canonical(g),'rows':rows,'evidence_refs':coords}

def write_matrix(path: Path,g: dict,summary=None):
    entities,before,after=graph_index(g)
    lines=['# Матрица трассируемости','', 'Проекция trace/graph.json. Исходный реестр — JSON; таблица не редактируется вручную.','',
           '| Test | Intent / hypothesis | BR / AC | ADR | FR / NFR | Story / code |','|---|---|---|---|---|---|']
    for tid in sorted(ids_of(g,{'E2E','CHECK'})):
        up=closure(before,tid)
        req=[i for i in up if entities[i]['kind'] in ['FR','NFR']]
        impl=set()
        for rid in req:
            impl.update(i for i in closure(after,rid) if entities[i]['kind'] in ['STORY','CODE'])
        def cell(k):return ', '.join(i for i in up if entities[i]['kind'] in k) or '—'
        lines.append('| '+ ' | '.join([tid,cell({'INT','HYP'}),cell({'BR','AC'}),cell({'ADR'}),cell({'FR','NFR'}),', '.join(sorted(impl)) or '—'])+' |')
    if summary:lines+=['','Runtime evidence coordinates (не выдуманные URL):','```json',json.dumps(summary['evidence_refs'],ensure_ascii=False,indent=2),'```']
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def inventory(w: Native):
    existing={}
    base=w.root/'pdlc/product'
    if base.is_dir():
        for p in sorted(base.rglob('*')):
            if p.is_file() and not p.is_symlink():existing[p.relative_to(base).as_posix()]=digest(p)
    data={'schema_version':VERSION,'run_id':w.run_id,'source_snapshot':w.snapshot(),
          'baseline_files':existing,'mode':w.binding.get('mode','auto'),'limitations':[], 'created_at':now()}
    save(w.out/'inventory.json',data);w.summary('on_success',[])

def freeze(w: Native,phase: str):
    # Approval itself is HG gate history; this is only the accepted artifact fingerprint.
    source_node='human-prd' if phase=='prd' else 'command-readiness'
    data={'schema_version':VERSION,'phase':phase,'subject_digest':w.subject(phase),'created_at':now(),
          'run_id':w.run_id,'origin_gate_node':source_node,'note':'Approval identity and action are native HG audit, not an agent assertion'}
    save(w.out/'freeze.json',data);w.summary('on_success',[])

def baseline_validate(w: Native):
    base=w.change/'baseline';facts=load(base/'facts.json');errors=[]
    if not facts.get('facts'):errors.append('No baseline facts; cannot recover invented history')
    inv=load(w.source('command-inventory','inventory.json'))
    if canonical(inv['source_snapshot'])!=canonical(w.snapshot()):errors.append('Baseline source changed after inventory')
    repo_roots={r['id']:inside(w.root,r['path'],dot=True) for r in w.registry()['repositories']}
    for f in facts.get('facts',[]):
        if f.get('origin') not in ['observed','confirmed','inferred']:errors.append('Baseline fact origin required')
        if not f.get('sources'):errors.append('Baseline fact sources required')
        for source in f.get('sources',[]):
            if source.get('repo') not in repo_roots:errors.append('Unknown baseline source repo');continue
            path=inside(repo_roots[source['repo']],source.get('path',''))
            if not path.is_file():errors.append('Baseline source file missing');continue
            if source.get('content_sha256')!=digest(path):errors.append('Baseline source checksum missing/stale')
            if not source.get('revision') or not source.get('anchor') or source['anchor'] not in path.read_text(encoding='utf-8'):
                errors.append('Baseline source revision/anchor missing')
        if f.get('origin')=='inferred' and f.get('normative') is True:errors.append('Inferred business motive cannot be normative')
    for f in ['index.md','business.md','architecture.md','architecture.dsl','SRS.md','test-model.json','facts.json']:
        p=base/f
        if not p.is_file():errors.append('Missing baseline file '+f)
        else:errors+=no_placeholders(p.read_text(encoding='utf-8'))
    data={'files':{p.relative_to(base).as_posix():digest(p) for p in base.rglob('*') if p.is_file()},'facts':facts}
    subject=canonical(data)
    r=load(w.source('ai-baseline-review','review.json'))
    if not {f['id'] for f in facts.get('facts',[])}<=set(r.get('checked_ids',[])):errors.append('Baseline review coverage incomplete')
    if any(f.get('severity') in ['blocking','critical','high'] for f in r.get('findings',[])):errors.append('Blocking baseline review findings')
    if r.get('role')!='pdlc-baseline-auditor' or r.get('verdict')!='pass' or r.get('subject_digest')!=subject:
        errors.append('Baseline review missing/failed/stale')
    save(w.out/'baseline-digest.json',{'subject_digest':subject,'files':data['files']})
    w.summary('on_rework' if errors else 'on_success',errors)

def baseline_seal(w: Native):
    approved=load(w.source('command-baseline-check','baseline-digest.json'))
    base=w.change/'baseline'
    for rel,expected in approved['files'].items():
        if digest(inside(base,rel))!=expected:raise ContractError('Baseline changed after its gate')
    inventory=load(w.source('command-inventory','inventory.json'))
    if canonical(inventory['source_snapshot'])!=canonical(w.snapshot()):raise ContractError('Source changed after baseline validation')
    existing=inventory['baseline_files']
    mapping={'index.md':'context.md','business.md':'business/overview.md','architecture.md':'architecture/architecture.md',
             'architecture.dsl':'architecture/architecture.dsl','SRS.md':'system/SRS.md','test-model.json':'tests/model.json','facts.json':'trace/facts.json'}
    for src,dst in mapping.items():
        target=inside(w.root/'pdlc/product',dst)
        actual=digest(target) if target.is_file() else None
        if actual!=existing.get(dst):raise ContractError('Concurrent product documentation modification/deletion: '+dst)
    for src,dst in mapping.items():
        target=inside(w.root/'pdlc/product',dst);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(base/src,target)
    w.summary('on_success',[],{'status':'baseline-prepared-not-merged','facts_policy':'observed/confirmed/inferred retained'})

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--version',action='version',version=VERSION)
    sub=p.add_subparsers(dest='action',required=True)
    sub.add_parser('catalog-root')
    x=sub.add_parser('seed-product');x.add_argument('--root',type=Path,default=Path.cwd())
    x=sub.add_parser('artifact-dir');x.add_argument('--node',required=True);x.add_argument('--root',type=Path,default=Path.cwd())
    x=sub.add_parser('init-binding');x.add_argument('--node',default='ai-intake');x.add_argument('--root',type=Path,default=Path.cwd());x.add_argument('--run-id',required=True);x.add_argument('--kind',choices=['feature','baseline'],default='feature');x.add_argument('--mode',choices=['auto','brownfield','greenfield'],default='auto')
    x=sub.add_parser('ai-summary');x.add_argument('--node',required=True);x.add_argument('--root',type=Path,default=Path.cwd());x.add_argument('--route',required=True);x.add_argument('--action',dest='action_text',required=True);x.add_argument('--rework-instruction',default='')
    x=sub.add_parser('validate-trace');x.add_argument('graph',type=Path);x.add_argument('--stage',choices=['prd','architecture','srs','ready','implemented','verified'],default='ready')
    x=sub.add_parser('impact');x.add_argument('graph',type=Path);x.add_argument('--id',required=True)
    x=sub.add_parser('matrix');x.add_argument('graph',type=Path);x.add_argument('--output',type=Path,required=True)
    x=sub.add_parser('junit');x.add_argument('report',type=Path);x.add_argument('--ids',nargs='+',required=True)
    for cmd in ['inventory','gate','freeze','run','subject','baseline-check','baseline-seal','baseline-subject']:
        x=sub.add_parser(cmd);x.add_argument('--node',required=True);x.add_argument('--root',type=Path,default=Path.cwd())
        if cmd=='gate':x.add_argument('--stage',required=True,choices=['prd','ready','code','verify','final']);x.add_argument('--controlled',action='store_true')
        if cmd=='freeze':x.add_argument('--phase',required=True,choices=['prd','design'])
        if cmd=='run':x.add_argument('--kind',required=True,choices=['checks','e2e'])
        if cmd=='subject':x.add_argument('--kind',required=True,choices=['prd','design','code','acceptance'])
    args=p.parse_args(argv)
    try:
        if args.action=='catalog-root':print(Path(__file__).resolve().parents[4]);return 0
        if args.action=='seed-product':
            base=Path(__file__).resolve().parents[4]/'skills/pdlc-contracts/2.0/assets/product/pdlc'
            if not base.is_dir():raise ContractError('Installed catalog assets missing')
            for source in base.rglob('*'):
                if source.is_file():
                    target=inside(args.root,'pdlc/'+source.relative_to(base).as_posix())
                    if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
            return 0
        if args.action in ['artifact-dir','init-binding']:
            if not re.fullmatch(r'[a-z0-9-]+',args.node):raise ContractError('Invalid node id')
            base=inside(args.root,'.hgsdlc/nodes/'+args.node)
            attempts=sorted([(int(p.name.split('-')[1]),p) for p in base.glob('attempt-*') if re.fullmatch(r'attempt-[0-9]+',p.name) and p.is_dir()])
            if not attempts:raise ContractError('Native current attempt is not allocated by HG')
            attempt,out=attempts[-1]
            if args.action=='artifact-dir':print(out);return 0
            if args.node!='ai-intake' or len(attempts)!=1:raise ContractError('Binding may be created only once, in ai-intake')
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{5,79}',args.run_id):raise ContractError('Unsafe run id')
            cid=('BASE-' if args.kind=='baseline' else 'CHG-')+args.run_id
            target=inside(args.root,'pdlc/changes/'+cid)
            binding={'schema_version':VERSION,'run_id':args.run_id,'change_id':cid,'change_dir':'pdlc/changes/'+cid,'mode':args.mode,'kind':args.kind}
            if (out/'binding.json').exists():
                if load(out/'binding.json')!=binding:raise ContractError('Immutable binding changed')
                print(out/'binding.json');return 0
            if target.exists():raise ContractError('Change directory collision; do not reuse a different run')
            target.mkdir(parents=True)
            save(out/'binding.json',binding);print(out/'binding.json');return 0
        if args.action=='validate-trace':
            errors=validate_graph(load(args.graph),args.stage);print(json.dumps({'errors':errors},indent=2,ensure_ascii=False));return int(bool(errors))
        if args.action=='impact':print(json.dumps(impact(load(args.graph),args.id),ensure_ascii=False,indent=2));return 0
        if args.action=='matrix':write_matrix(args.output,load(args.graph));return 0
        if args.action=='junit':
            results,errors=parse_junit(args.report,set(args.ids));print(json.dumps({'results':results,'errors':errors},indent=2));return int(bool(errors))
        w=Native(args.root,args.node)
        if args.action=='ai-summary':
            if not re.fullmatch(r'on_[a-z_]+',args.route):raise ContractError('Invalid route')
            summary={'step_id':w.node,'attempt':w.attempt,'status':'done','route':args.route,'actions':[args.action], 'rework_instruction':args.rework_instruction}
            summary['actions']=[args.action_text] if hasattr(args,'action_text') else ['AI artifact step completed']
            save(w.out/'step-summary.json',summary)
            print('STEP_SUMMARY:\n```json\n'+json.dumps(summary,ensure_ascii=False)+'\n```');return 0
        if args.action=='subject':print(w.subject(args.kind));return 0
        if args.action=='baseline-subject':
            base=w.change/'baseline'; print(canonical({'files':{p.relative_to(base).as_posix():digest(p) for p in base.rglob('*') if p.is_file()},'facts':load(base/'facts.json')}));return 0
        try:
            if args.action=='inventory':inventory(w)
            elif args.action=='gate':gate(w,args.stage,args.controlled)
            elif args.action=='freeze':freeze(w,args.phase)
            elif args.action=='run':run_tests(w,args.kind)
            elif args.action=='baseline-check':baseline_validate(w)
            elif args.action=='baseline-seal':baseline_seal(w)
        except (ContractError,OSError,ValueError,KeyError,TypeError) as exc:
            # Known contract failure is a negative artifact, not a successful test.
            # Fatal adapter init errors never get converted into on_success.
            w.summary('on_blocked',[str(exc)])
        return 0  # node executed; HG chooses on_success/on_rework/on_blocked from summary
    except (ContractError,OSError,ValueError,KeyError,TypeError) as exc:
        print('PDLC adapter failure: '+str(exc),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
