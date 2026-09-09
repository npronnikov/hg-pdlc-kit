#!/usr/bin/env python3
"""PDLC 3.0 finite checks. No HG state, attempt counters, scheduler, or native-directory discovery.
Run artifacts use logical filenames, materialized by HG as in the supplied command-node examples.
Python >=3.10, standard library only. Execute in the monorepo root.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, signal, subprocess, sys, time, uuid
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

VERSION = '3.0'
FRAGMENTS = {'prd': ['intent'], 'design': ['intent','architecture','system','tests','stories'],
             'code': ['intent','architecture','system','tests','stories','code'],
             'final': ['intent','architecture','system','tests','stories','code','evidence']}
FILES = {'prd':['intent.md','analysis.md','sources.json','PRD.md','decisions.md','trace/intent.json'],
         'design':['architecture.md','architecture.dsl','adr.md','SRS.md','contracts/index.md',
                   'test-model.md','test-model.feature','stories.md','verification-plan.json','risk.json',
                   'trace/architecture.json','trace/system.json','trace/tests.json','trace/stories.json']}
KINDS = {'INT','HYP','BR','AC','ADR','FR','NFR','STORY','CODE','E2E','CHECK','RUN','RESULT'}
RELATIONS = {('INT','motivates','HYP'),('HYP','justifies','BR'),('BR','accepted_by','AC'),
 ('BR','realized_by','ADR'),('BR','specified_by','FR'),('BR','specified_by','NFR'),
 ('ADR','constrains','FR'),('ADR','constrains','NFR'),('FR','verified_by','E2E'),
 ('FR','verified_by','CHECK'),('NFR','verified_by','E2E'),('NFR','verified_by','CHECK'),
 ('AC','verified_by','E2E'),('FR','implemented_by','STORY'),('NFR','implemented_by','STORY'),
 ('STORY','changes','CODE'),('CODE','exercised_by','E2E'),('CODE','exercised_by','CHECK'),
 ('E2E','evidenced_by','RESULT'),('CHECK','evidenced_by','RESULT'),('RUN','includes','RESULT')}
RISK_FLAGS = ['authorization_changes','sensitive_data_changes','destructive_migration',
              'public_contract_break','new_external_dependency','production_access']
RUN_NAMES = {'setup-report.json','prd-check.json','design-check.json','code-check.json',
 'build-report.json','build.stdout.log','build.stderr.log','e2e-report.json','e2e-results.xml',
 'e2e.stdout.log','e2e.stderr.log','seal-prd.json','seal-design.json','finalize-report.json',
 'baseline-check.json','baseline-seal.json','bootstrap-review.json','questions.md','interview.md',
 'prd-review.json','readiness-review.json','code-review.json','test-review.json','acceptance-review.json',
 'build-review.json','step-summary.json'}

def now(): return datetime.now(timezone.utc).isoformat()
def digest_bytes(b: bytes): return hashlib.sha256(b).hexdigest()
def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(path: Path): return json.loads(path.read_text(encoding='utf-8'))
def safe(root: Path, path: str) -> Path:
    root = root.resolve()
    p = Path(path)
    if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe project path: '+path)
    resolved = (root/p).resolve()
    if not resolved.is_relative_to(root): raise ValueError('Path/symlink escapes monorepo: '+path)
    return resolved

def bundle(root: Path, change: Path, stage: str):
    root = root.resolve()
    change = change.resolve()
    names = FILES['prd'] + (FILES['design'] if stage != 'prd' else [])
    # Contracts are normative; seal every real contract, not only their index.
    if stage != 'prd': names += [str(p.relative_to(change)) for p in sorted((change/'contracts').rglob('*')) if p.is_file()]
    values = {}
    for name in sorted(set(names)):
        p=safe(root,str((change/name).relative_to(root)))
        if not p.is_file(): raise ValueError('Missing sealed input: '+str(p.relative_to(root)))
        values[str(p.relative_to(root))]=digest_bytes(p.read_bytes())
    return digest_bytes(json.dumps(values,sort_keys=True).encode()),values

def check_seal(root,change,stage):
    p=change/'approvals'/f'{stage}.json'
    if not p.is_file(): raise ValueError('Missing approval: '+str(p.relative_to(root)))
    record=load(p); current,_=bundle(root,change,stage)
    if record.get('bundle_digest')!=current: raise ValueError('Approved '+stage+' inputs changed; return through the owning gate')
    return record

def scan_source(root: Path):
    try:
        r=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=root,
                         capture_output=True,check=True,timeout=15)
        paths=[root/os.fsdecode(n) for n in r.stdout.split(b'\0') if n]
    except (OSError,subprocess.SubprocessError):
        paths=list(root.rglob('*'))
    result={}
    for p in sorted(set(paths)):
        rel=p.relative_to(root)
        if set(rel.parts)&{'.git','.hgsdlc','__pycache__','node_modules','.venv','.pytest_cache','playwright-report','test-results'}: continue
        if rel.parts[0]=='pdlc' or str(rel) in RUN_NAMES or p.suffix=='.pyc': continue
        if p.is_file(): result[str(rel)]=digest_bytes(safe(root,str(rel)).read_bytes())
    return digest_bytes(json.dumps(result,sort_keys=True).encode()),result

def section(text: str, anchor: str):
    marker=f'<a id="{anchor}"></a>'
    if marker not in text: raise ValueError('Missing exact anchor '+anchor)
    tail=text.split(marker,1)[1]
    return tail.split('<a id="',1)[0].strip()

def validate_plan(plan):
    for suite in ('build','e2e'):
        item=plan.get(suite,{})
        argv=item.get('argv')
        if not isinstance(argv,list) or not argv or not all(isinstance(x,str) and x for x in argv):
            raise ValueError(suite+': argv must be a nonempty string array')
        if Path(argv[0]).name in {'sh','bash','zsh','cmd','powershell','pwsh'} or '-c' in argv:
            raise ValueError('Shell/eval command is not allowed in verification-plan')
        if type(item.get('timeout_seconds')) is not int or not 1<=item['timeout_seconds']<=1800:
            raise ValueError('Finite timeout_seconds 1..1800 is required')
        cwd=Path(item.get('cwd','.'))
        if cwd.is_absolute() or '..' in cwd.parts: raise ValueError('Suite cwd escapes monorepo')
    if not any('{junit}' in x for x in plan['e2e']['argv']): raise ValueError('E2E argv requires a {junit} output argument')
    if plan.get('boundary') not in {'browser-system','api-system','cli-system','mixed-system'}:
        raise ValueError('Declare the real E2E system boundary')
    if not isinstance(plan.get('in_scope_components'),list) or not plan['in_scope_components']:
        raise ValueError('List real in_scope_components; component tests are not E2E')
    if plan.get('internal_mocks') is not False: raise ValueError('Internal product mocks are forbidden in the E2E acceptance suite')


def check(root: Path, change: Path, stage: str):
    errors=[]; nodes=[]; edges=[]; previous={}
    old=change/'trace/graph.json'
    if old.is_file(): previous={n['id']:n for n in load(old).get('nodes',[]) if 'id' in n}
    for frag in FRAGMENTS[stage]:
        try:
            data=load(change/'trace'/f'{frag}.json')
            if data.get('schema_version')!=VERSION: raise ValueError('schema_version must be 3.0')
            if not isinstance(data.get('nodes'),list) or not isinstance(data.get('edges'),list): raise ValueError('nodes/edges must be arrays')
            nodes.extend(data['nodes']);edges.extend(data['edges'])
        except (OSError,ValueError,TypeError) as e: errors.append(f'{frag}: {e}')
    by={}
    for n in nodes:
        try:
            i=n['id'];kind=n['kind']
            if not isinstance(i,str) or not re.fullmatch(r'[A-Z][A-Za-z0-9-]{2,99}',i): raise ValueError('Invalid stable ID')
            if i in by: raise ValueError('Duplicate ID '+i)
            if kind not in KINDS: raise ValueError('Unknown kind '+str(kind))
            if type(n.get('revision')) is not int or n['revision']<1: raise ValueError('Positive integer revision required')
            if not isinstance(n.get('statement'),str) or len(n['statement'].strip())<12: raise ValueError('Atomic statement required')
            if re.search(r'\b(TBD|TODO|FIXME|PLACEHOLDER)\b',n['statement'],re.I): raise ValueError('Unresolved statement')
            artifact=n['artifact']; p=safe(root,artifact['path'])
            if not p.is_file(): raise ValueError('Source does not exist: '+artifact['path'])
            if kind=='CODE': content=p.read_text(encoding='utf-8')
            else: content=section(p.read_text(encoding='utf-8'),artifact['anchor'])
            if kind not in {'CODE','RUN','RESULT'} and n['statement'] not in content: raise ValueError('Statement differs from its authoritative document section')
            if kind=='E2E':
                if n.get('boundary') not in {'browser-system','api-system','cli-system'}: raise ValueError('Explicit E2E boundary required')
                for key in ('preconditions','test_data','steps','expected'):
                    if not n.get(key): raise ValueError('E2E missing '+key)
            if kind=='NFR' and not n.get('measurement'): raise ValueError('NFR needs metric, condition and threshold in measurement')
            payload={k:v for k,v in n.items() if k!='content_hash'}
            payload['authoritative_content']=content
            n['content_hash']=digest_bytes(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode())
            prev=previous.get(i)
            if prev and prev.get('revision')==n['revision'] and prev.get('content_hash') and prev['content_hash']!=n['content_hash']:
                errors.append(i+': content changed without incrementing revision')
            by[i]=n
        except (OSError,ValueError,TypeError,KeyError) as e: errors.append(str(n.get('id','?'))+': '+str(e))
    seen=set()
    for e in edges:
        try:
            a,b=e['from'],e['to'];rel=e['relation'];key=(a,rel,b)
            if key in seen: raise ValueError('Duplicate edge')
            seen.add(key)
            if a not in by or b not in by: raise ValueError('Orphan edge')
            if (by[a]['kind'],rel,by[b]['kind']) not in RELATIONS: raise ValueError('Invalid direction/type')
            if e.get('from_revision')!=by[a]['revision'] or e.get('to_revision')!=by[b]['revision']: raise ValueError('Stale edge revision')
        except (ValueError,TypeError,KeyError) as ex: errors.append(f'edge {e}: {ex}')
    required={'INT','HYP','BR','AC'}
    if stage!='prd':required|={'ADR','FR','NFR','STORY','E2E'}
    if stage in ('code','final'):required|={'CODE'}
    if stage=='final':required|={'RUN','RESULT'}
    for k in sorted(required-{n.get('kind') for n in nodes}):errors.append('Missing entity kind '+k)
    obligations={'INT':[{'motivates'}],'HYP':[{'justifies'}],'BR':[{'accepted_by'}]}
    if stage!='prd':obligations.update({'BR':[{'accepted_by'},{'realized_by'},{'specified_by'}],
        'AC':[{'verified_by'}],'ADR':[{'constrains'}],'FR':[{'verified_by'},{'implemented_by'}],
        'NFR':[{'verified_by'}]})
    if stage in ('code','final'):obligations.update({'STORY':[{'changes'}],'CODE':[{'exercised_by'}]})
    if stage=='final':obligations.update({'E2E':[{'evidenced_by'}],'CHECK':[{'evidenced_by'}],'RUN':[{'includes'}]})
    for i,n in by.items():
        outgoing={e.get('relation') for e in edges if e.get('from')==i and e.get('to') in by}
        for options in obligations.get(n['kind'],[]):
            if not outgoing&options: errors.append(i+': missing outgoing relation '+','.join(options))
        if n['kind'] not in {'INT','RUN'} and not any(e.get('to')==i and e.get('from') in by for e in edges):
            errors.append(i+': ungrounded entity (no incoming justification)')
    try:
        input_digest,_=bundle(root,change,'prd' if stage=='prd' else 'design')
        if stage!='prd':
            check_seal(root,change,'prd');validate_plan(load(change/'verification-plan.json'))
            risk=load(change/'risk.json')
            if set(risk.get('flags',{}))!=set(RISK_FLAGS): raise ValueError('Complete explicit risk flags required')
            if not all(type(v) is bool for v in risk['flags'].values()): raise ValueError('Unknown risk is not false; escalate to human')
        if stage in ('code','final'):
            check_seal(root,change,'design')
            mapping=load(change/'implementation-map.json')
            planned={n['id'] for n in nodes if n['kind']=='STORY'}
            covered=set()
            for item in mapping.get('changes',[]):
                if not item.get('story_ids') or not set(item['story_ids'])<=planned:raise ValueError('Implementation map has unknown/missing story IDs')
                covered.update(item['story_ids'])
                if not item.get('paths'):raise ValueError('Implementation entry requires real paths')
                for path in item['paths']:
                    if not safe(root,path).is_file():raise ValueError('Missing implemented path '+path)
            if covered!=planned:raise ValueError('Not every story has implemented paths')
            if not any(n['kind']=='CODE' and not n['artifact']['path'].startswith('pdlc/') for n in nodes):raise ValueError('No real product code')
        if stage=='final':assert_verified(root,change)
    except (OSError,ValueError,TypeError,KeyError) as e:
        input_digest=None;errors.append(str(e))
    result={'schema_version':VERSION,'stage':stage,'status':'passed' if not errors else 'failed',
            'bundle_digest':input_digest,'errors':errors,'node_count':len(nodes),'edge_count':len(edges),'checked_at':now()}
    dump(change/'trace/graph.json',{'schema_version':VERSION,'valid':not errors,'stage':stage,'nodes':nodes,'edges':edges})
    lines=['# Матрица трассируемости','','Машинный источник — stage-фрагменты; этот файл генерируется проверкой.',
           '', '| Основание | Связь | Результат | Ревизии |','|---|---|---|---|']
    lines += [f"| {e.get('from')} | {e.get('relation')} | {e.get('to')} | {e.get('from_revision')} → {e.get('to_revision')} |" for e in edges]
    lines += ['', 'Проверка: '+result['status']]+['- '+e for e in errors]
    (change/'trace/matrix.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return result

def parse_junit(path: Path, expected: set[str]):
    statuses={};errors=[]
    try:
        if path.stat().st_size>20_000_000:raise ValueError('JUnit too large')
        raw=path.read_text(encoding='utf-8')
        if '<!DOCTYPE' in raw.upper() or '<!ENTITY' in raw.upper():raise ValueError('DTD/entities are forbidden')
        root=ET.fromstring(raw)
        for case in root.iter('testcase'):
            matches=re.findall(r'\[(E2E-[A-Za-z0-9-]+|CHECK-[A-Za-z0-9-]+)\]',case.get('name',''))
            if len(matches)!=1:errors.append('Each testcase needs exactly one [E2E-ID] or [CHECK-ID]');continue
            i=matches[0]
            if i in statuses:errors.append('Duplicate test ID '+i)
            status='passed'
            if case.find('skipped') is not None:status='skipped'
            if case.find('failure') is not None or case.find('error') is not None:status='failed'
            statuses[i]=status
        for i in sorted(expected-set(statuses)):errors.append('Missing test '+i)
        for i in sorted(set(statuses)-expected):errors.append('Unexpected test '+i)
        for i,s in statuses.items():
            if s!='passed':errors.append(i+': '+s)
        if not statuses:errors.append('Empty test run is not success')
    except (OSError,ValueError,ET.ParseError) as e:errors.append('JUnit: '+str(e))
    return statuses,errors

def execute(root: Path, argv: list[str], cwd: str, timeout: int, out: Path, err: Path):
    started=time.monotonic();rc=None;failure=None
    with out.open('w',encoding='utf-8') as stdout,err.open('w',encoding='utf-8') as stderr:
        try:
            proc=subprocess.Popen(argv,cwd=safe(root,cwd),stdout=stdout,stderr=stderr,
                                  stdin=subprocess.DEVNULL,start_new_session=True)
            try:rc=proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGKILL);proc.wait();failure='timeout';rc=124
        except OSError as e:failure=str(e);rc=127
    return {'exit_code':rc,'failure':failure,'elapsed_seconds':round(time.monotonic()-started,4)}

def run_suite(root,change,suite,run_id):
    report={'schema_version':VERSION,'status':'blocked','errors':[],'suite':suite,'started_at':now(),
            'execution_id':str(uuid.uuid4()),'run_id':run_id,'node_id':'command-'+suite}
    out=root/(suite+'.stdout.log');err=root/(suite+'.stderr.log')
    out.write_text('');err.write_text('')
    junit=root/'e2e-results.xml'
    if suite=='e2e':junit.unlink(missing_ok=True)
    try:
        check_seal(root,change,'prd');check_seal(root,change,'design')
        plan=load(change/'verification-plan.json');validate_plan(plan)
        before,files=scan_source(root);spec=plan[suite]
        argv=[x.replace('{junit}',str(junit)) for x in spec['argv']]
        report.update({'argv':argv,'boundary':plan['boundary'],'source_digest':before,'source_files':files})
        report.update(execute(root,argv,spec.get('cwd','.'),spec['timeout_seconds'],out,err))
        after,_=scan_source(root)
        if before!=after:report['errors'].append('Product/test sources changed during verification')
        if report['exit_code']!=0:report['errors'].append('Actual process exit '+str(report['exit_code']))
        if suite=='e2e':
            tests=load(change/'trace/tests.json')['nodes']
            expected={n['id'] for n in tests if n['kind'] in {'E2E','CHECK'}}
            statuses,errors=parse_junit(junit,expected);report['errors']+=errors;report['tests']=statuses
            # Only actual emitted results become RESULT entities; missing tests are never fabricated.
            report['test_definition_digest']=digest_bytes((change/'trace/tests.json').read_bytes())
            report['implementation_digest']=digest_bytes((change/'implementation-map.json').read_bytes())
            report['e2e_map_digest']=digest_bytes((change/'e2e-map.json').read_bytes())
            testmap=load(change/'e2e-map.json')
            if set(testmap.get('tests',{}))!=expected:report['errors'].append('E2E map IDs differ from test model')
            for i,paths in testmap.get('tests',{}).items():
                if not paths or not all(i in safe(root,p).read_text(encoding='utf-8') for p in paths):
                    report['errors'].append(i+': executable source missing ID')
        report['status']='passed' if not report['errors'] else 'failed'
    except (OSError,ValueError,TypeError,KeyError) as e:report['errors'].append(str(e))
    if suite=='e2e' and not junit.is_file():
        # Diagnostic only: no testcase and no invented E2E outcome. parse_junit will reject this.
        elem=ET.Element('testsuite',name='harness-diagnostic',tests='0',errors='1')
        ET.SubElement(elem,'system-err').text='Harness produced no JUnit; blocked, not passed.'
        ET.ElementTree(elem).write(junit,encoding='utf-8',xml_declaration=True)
    report['finished_at']=now()
    report['raw_artifacts']=[{'scope':'run','run_id':run_id,'node_id':'command-'+suite,
         'execution_id':report['execution_id'],'path':p.name,'sha256':digest_bytes(p.read_bytes())}
         for p in [out,err]+([junit] if suite=='e2e' else [])]
    if suite=='e2e':
        dump(change/'verification.json',report)
        lines=['# Фактическая проверка','','Это результат локального процесса, не подтверждение бизнес-эффекта.',
               '',f'<a id="RUN-{run_id}"></a>',f'Запуск {report["execution_id"]}; состояние {report["status"]}.']
        nodes=[{'id':'RUN-'+run_id,'kind':'RUN','revision':1,'statement':'Запуск исполняемой сквозной проверки системы.',
                'artifact':{'path':str((change/'verification.md').relative_to(root)),'anchor':'RUN-'+run_id}}];edges=[]
        current={n['id']:n for n in load(change/'trace/tests.json')['nodes']} if (change/'trace/tests.json').exists() else {}
        for i,status in report.get('tests',{}).items():
            rid='RESULT-'+i;lines += ['',f'<a id="{rid}"></a>',f'{i}: {status}.']
            nodes.append({'id':rid,'kind':'RESULT','revision':1,'statement':f'Фактический результат {i}: {status}.',
                          'artifact':{'path':str((change/'verification.md').relative_to(root)),'anchor':rid},'status':status})
            if i in current:edges.append({'from':i,'to':rid,'relation':'evidenced_by','from_revision':current[i]['revision'],'to_revision':1})
            edges.append({'from':'RUN-'+run_id,'to':rid,'relation':'includes','from_revision':1,'to_revision':1})
        # Evidence changes on a new execution; retain stable IDs but bump revisions, update local links.
        oldpath=change/'trace/evidence.json'
        olds={n['id']:n for n in load(oldpath).get('nodes',[])} if oldpath.exists() else {}
        for n in nodes:
            if n['id'] in olds:n['revision']=olds[n['id']]['revision']+1
        revisions={n['id']:n['revision'] for n in nodes}
        for e in edges:
            if e['from'] in revisions:e['from_revision']=revisions[e['from']]
            if e['to'] in revisions:e['to_revision']=revisions[e['to']]
        (change/'verification.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        dump(oldpath,{'schema_version':VERSION,'nodes':nodes,'edges':edges})
    return report

def assert_verified(root,change):
    v=load(change/'verification.json')
    if v.get('status')!='passed' or v.get('exit_code')!=0 or v.get('errors'):raise ValueError('E2E evidence is not passed')
    if scan_source(root)[0]!=v.get('source_digest'):raise ValueError('Code/test sources changed after E2E')
    for name,key in [('trace/tests.json','test_definition_digest'),('implementation-map.json','implementation_digest'),('e2e-map.json','e2e_map_digest')]:
        if digest_bytes((change/name).read_bytes())!=v.get(key):raise ValueError(name+' changed after E2E')
    tests={n['id'] for n in load(change/'trace/tests.json')['nodes'] if n['kind'] in {'E2E','CHECK'}}
    if set(v.get('tests',{}))!=tests or any(s!='passed' for s in v['tests'].values()):raise ValueError('Test coverage/outcomes are incomplete')
    check_seal(root,change,'prd');check_seal(root,change,'design')
    return v

def seal(root,change,stage,expected,authority,run_id):
    actual,hashes=bundle(root,change,stage)
    if actual!=expected:raise ValueError('Documents changed after the reviewed digest; approval cannot be transferred')
    if stage=='design':
        check_seal(root,change,'prd')
        if authority=='policy':
            flags=load(change/'risk.json')['flags']
            if set(flags)!=set(RISK_FLAGS) or any(type(v) is not bool or v for v in flags.values()):raise ValueError('Human technical decision is mandatory for this risk')
    if stage=='prd' and authority!='human':raise ValueError('Only the product owner approves intent')
    value={'schema_version':VERSION,'stage':stage,'authority':authority,'run_id':run_id,
           'decision_node':('human-prd-approval' if stage=='prd' else 'human-design-approval') if authority=='human' else 'ai-readiness',
           'bundle_digest':actual,'files':hashes,'recorded_at':now(),
           'notice':'Decision provenance comes from the native HG transition; this file is not a second gate.'}
    p=change/'approvals'/f'{stage}.json'
    if p.exists():
        old=load(p);history=change/'approvals'/f'{stage}-history.json';records=load(history) if history.exists() else []
        records.append(old);dump(history,records)
    dump(p,value);return {'status':'passed','bundle_digest':actual}

def baseline_check(root):
    base=root/'pdlc/product';required=['index.md','business.md','architecture.md','architecture.dsl','system.md','test-model.md','sources.json','trace.json']
    errors=[]
    for name in required:
        if not (base/name).is_file():errors.append('Missing baseline file '+name)
    if not errors:
        facts=load(base/'sources.json').get('facts',[])
        if not facts:errors.append('Baseline has no sourced facts')
        for f in facts:
            if f.get('classification') not in {'observed','documented','inferred','unknown'}:errors.append('Missing fact classification')
            if f.get('classification') in {'observed','documented'}:
                p=safe(root,f.get('path',''))
                if not p.is_file():errors.append('Missing fact source '+str(f.get('path')))
                elif f.get('sha256')!=digest_bytes(p.read_bytes()):errors.append('Stale fact source '+str(f.get('path')))
            if f.get('classification')=='inferred' and f.get('approved') is True:errors.append('Inference cannot auto-approve business intent')
    files={n:digest_bytes((base/n).read_bytes()) for n in required if (base/n).is_file()}
    return {'status':'failed' if errors else 'passed','errors':errors,'bundle_digest':digest_bytes(json.dumps(files,sort_keys=True).encode())}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['check','seal','run','finalize','baseline-check','baseline-seal'])
    p.add_argument('--change');p.add_argument('--stage',default='prd',choices=FRAGMENTS)
    p.add_argument('--suite',choices=['build','e2e']);p.add_argument('--report',required=True)
    p.add_argument('--expected-digest');p.add_argument('--authority',choices=['human','policy'],default='human')
    p.add_argument('--run-id',default='local-demonstration');a=p.parse_args(argv);root=Path.cwd().resolve()
    try:
        report_path=safe(root,a.report)
        if a.report not in RUN_NAMES:raise ValueError('Use a declared logical run output filename')
        if a.action.startswith('baseline'):
            result=baseline_check(root)
            if a.action=='baseline-seal':
                if result['status']!='passed' or result['bundle_digest']!=a.expected_digest:raise ValueError('Baseline changed or is incomplete')
                dump(root/'pdlc/product/baseline.json',{'status':'accepted-as-observed','bundle_digest':result['bundle_digest'],'run_id':a.run_id,
                    'notice':'Business inferences remain inferred; this does not manufacture a historical PRD.'})
        else:
            if not a.change or not re.fullmatch(r'pdlc/changes/[A-Za-z0-9][A-Za-z0-9-]{0,99}',a.change):raise ValueError('A monorepo-relative pdlc/changes/<id> is required')
            change=safe(root,a.change)
            if a.action=='check':result=check(root,change,a.stage)
            elif a.action=='run':
                if a.suite is None:raise ValueError('--suite is required')
                result=run_suite(root,change,a.suite,a.run_id)
            elif a.action=='seal':result=seal(root,change,a.stage,a.expected_digest,a.authority,a.run_id)
            else:
                result=check(root,change,'final')
                if result['status']!='passed':raise ValueError('; '.join(result['errors']))
                acceptance=load(change/'acceptance.json')
                if acceptance.get('verdict')!='accepted' or acceptance.get('blocking_findings'):raise ValueError('Independent acceptance has blockers')
                v=assert_verified(root,change)
                (change/'delivery.md').write_text('# Проверенная реализация\n\nСтатус: **verified-not-integrated**.\n\n'
                     f'Реальный E2E execution: {v["execution_id"]}. Passed: {len(v["tests"])}.\n\n'
                     'См. PRD.md, SRS.md, trace/matrix.md, verification.json и acceptance.json.\n'
                     'Никаких merge, push, deploy и выводов о бизнес-эффекте этот flow не делает.\n',encoding='utf-8')
        dump(report_path,result)
        print(json.dumps({'status':result.get('status'),'report':a.report},ensure_ascii=False))
        # Expected check/test failures are data. The next AI node MUST route rework/blocked.
        # Finalization and malformed command contracts, in contrast, fail closed with nonzero.
        return 0
    except Exception as e:
        try:dump(safe(root,a.report),{'status':'blocked','errors':[str(e)],'checked_at':now()})
        except Exception:pass
        print('PDLC: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
