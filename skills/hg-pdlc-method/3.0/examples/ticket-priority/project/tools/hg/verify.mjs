/** Deterministic product checker. No graph, agents, gates, retries or workflow state. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function must(v,m){if(!v) throw new Error(m);}
function safe(p){
  must(typeof p==='string' && p && !path.isAbsolute(p),'Expected relative project path');
  const q=path.resolve(root,p);must(q.startsWith(root+path.sep),'Path escapes monorepo: '+p);
  if(fs.existsSync(q)){const real=fs.realpathSync(q);must(real.startsWith(root+path.sep),'Symlink escapes monorepo: '+p);}
  return q;
}
const read=p=>JSON.parse(fs.readFileSync(safe(p),'utf8'));
const hashFile=p=>sha(fs.readFileSync(safe(p)));
const put=(p,o)=>fs.writeFileSync(safe(p),JSON.stringify(o,null,2)+'\n');
function input(p){const x=read(p);must(/^CHG-[a-z0-9-]{1,100}$/.test(x.change_id),'Invalid change_id');return x;}
function folder(i){return 'docs/changes/'+i.change_id;}
function listDir(rel){
 if(!fs.existsSync(safe(rel)))return [];
 const out=[];
 for(const d of fs.readdirSync(safe(rel),{withFileTypes:true})){const p=rel+'/'+d.name;if(d.isDirectory())out.push(...listDir(p));else out.push(p);}
 return out.sort();
}
// Implements precisely the keyword subset used by the bundled schemas, not a general JSON Schema engine.
export function schemaCheck(v,s,loc='$'){
 const supported=new Set(['$schema','title','type','properties','required','additionalProperties','items','minItems','minLength','pattern','enum','minimum']);
 for(const k of Object.keys(s))must(supported.has(k),'Unsupported schema keyword '+k);
 if(s.enum)must(s.enum.some(x=>JSON.stringify(x)===JSON.stringify(v)),loc+': invalid enum');
 if(s.type){
  const ok=s.type==='array'?Array.isArray(v):s.type==='object'?v!==null&&typeof v==='object'&&!Array.isArray(v):s.type==='integer'?Number.isInteger(v):s.type==='number'?typeof v==='number'&&Number.isFinite(v):typeof v===s.type;
  must(ok,loc+': expected '+s.type);
 }
 if(s.type==='object'){
  for(const k of s.required||[])must(Object.hasOwn(v,k),loc+': missing '+k);
  for(const [k,x] of Object.entries(v)){
   if(Object.hasOwn(s.properties||{},k))schemaCheck(x,s.properties[k],loc+'.'+k);
   else if(s.additionalProperties===false)throw new Error(loc+': unknown property '+k);
   else if(typeof s.additionalProperties==='object')schemaCheck(x,s.additionalProperties,loc+'.'+k);
  }
 }
 if(s.type==='array'){if(s.minItems!==undefined)must(v.length>=s.minItems,loc+': too few items');v.forEach((x,i)=>schemaCheck(x,s.items,loc+'['+i+']'));}
 if(s.type==='string'){if(s.minLength)must(v.length>=s.minLength,loc+': empty');if(s.pattern)must(new RegExp(s.pattern).test(v),loc+': pattern');}
 if(s.minimum!==undefined)must(v>=s.minimum,loc+': minimum');
}
function unique(items,label){const m=new Map();for(const x of items){must(!m.has(x.id),'Duplicate '+label+' '+x.id);m.set(x.id,x);}return m;}
function refs(ids,map,label){must(ids.length===new Set(ids).size,'Duplicate reference '+label);for(const id of ids)must(map.has(id),'Unknown '+label+' '+id);}
export function validateSpec(i){
 const d=folder(i),names=['business','components','system','test-model','implementation-plan'],data={};
 for(const n of names){data[n]=read(d+'/'+n+'.json');schemaCheck(data[n],read('tools/hg/schemas/'+n+'.schema.json'));must(data[n].change_id===i.change_id,'Cross-change mismatch '+n);}
 const b=unique(data.business.business_requirements,'BR'),a=unique(data.business.acceptance_criteria,'AC'),s=unique(data.system.requirements,'SR'),c=unique(data.components.components,'CMP'),e=unique(data['test-model'].scenarios,'E2E'),t=unique(data['implementation-plan'].tasks,'TASK');
 for(const x of b.values()){
  refs(x.acceptance_ids,a,'AC');
  for(const id of x.acceptance_ids)must(a.get(id).business_ids.includes(x.id),'Asymmetric BR/AC '+x.id+'/'+id);
 }
 for(const x of a.values()){
  refs(x.business_ids,b,'BR');
  for(const id of x.business_ids)must(b.get(id).acceptance_ids.includes(x.id),'Asymmetric AC/BR '+x.id+'/'+id);
  must([...s.values()].some(y=>y.acceptance_ids.includes(x.id)),'AC lacks SR '+x.id);
  must([...e.values()].some(y=>y.required&&y.acceptance_ids.includes(x.id)),'AC lacks required E2E '+x.id);
 }
 for(const x of c.values()){refs(x.dependencies,c,'CMP dependency');x.repo_paths.forEach(safe);}
 for(const x of s.values()){
  refs(x.business_ids,b,'BR');refs(x.acceptance_ids,a,'AC');refs(x.component_ids,c,'CMP');
  for(const ac of x.acceptance_ids)must(a.get(ac).business_ids.some(br=>x.business_ids.includes(br)),'SR unrelated to AC business '+x.id);
  must([...t.values()].some(y=>y.system_ids.includes(x.id)),'SR lacks task '+x.id);
 }
 for(const x of e.values()){
  refs(x.acceptance_ids,a,'AC');refs(x.system_ids,s,'SR');safe(x.test_file);
  must(x.chain.length>=2,'E2E chain too short '+x.id);
  for(const ac of x.acceptance_ids)must(x.system_ids.some(id=>s.get(id).acceptance_ids.includes(ac)),'E2E/SR/AC mismatch '+x.id);
 }
 const color=new Map();
 function visit(id){must(color.get(id)!==1,'Task dependency cycle '+id);if(color.get(id)===2)return;color.set(id,1);for(const dep of t.get(id).depends_on)visit(dep);color.set(id,2);}
 for(const x of t.values()){refs(x.depends_on,t,'TASK');refs(x.system_ids,s,'SR');x.files.forEach(safe);}
 for(const id of t.keys())visit(id);
 const resources=data['implementation-plan'].protected_resources;
 must(Object.keys(resources).length>0,'No protected validation resources');
 must(Object.hasOwn(resources,'tools/hg/verify.mjs'),'Validator hash missing');
 for(const [p,h] of Object.entries(resources))must(hashFile(p)===h,'Protected resource changed '+p);
 for(const n of ['prd.md','architecture.md','srs.md','test-model.md','implementation-plan.md']){
  const text=fs.readFileSync(safe(d+'/'+n),'utf8');must(text.length>100,'Incomplete document '+n);
  must(!/REPLACE_WITH|<Название фичи>|BLOCKED: adapt/.test(text),'Unfilled template '+n);
 }
 const approval=read(d+'/approval-record.json');
 must(approval.gate==='human-prd'&&approval.decision==='approved','Missing PRD gate approval');
 must(approval.prd_sha256===hashFile(d+'/prd.md'),'PRD changed after approval');
 must(approval.business_sha256===hashFile(d+'/business.json'),'BR/AC changed after approval');
 const arch=read(d+'/architecture-approval.json');
 must(arch.architecture_sha256===hashFile(d+'/architecture.md'),'Architecture changed after review/approval');
 must(['risk_adaptive','governed'].includes(arch.mode),'Unknown approval mode');
 if(arch.requires_human||arch.mode==='governed')must(arch.decision==='approved'&&arch.gate==='human-architecture','Missing technical approval');
 else must(arch.decision==='not_required','Invalid risk-adaptive approval');
 return {d,data,b,a,s,c,e,t};
}
const contractNames=['prd.md','business.json','decisions.md','architecture.md','context.mmd','containers.mmd','sequence.mmd','components.json','approval-record.json','architecture-approval.json','srs.md','system.json','contracts-index.md','test-model.md','test-model.json','scenarios.feature','implementation-plan.md','implementation-plan.json'];
export function snapshot(i){
 const rootGit=execFileSync('git',['rev-parse','--show-toplevel'],{encoding:'utf8',cwd:root}).trim();
 must(fs.realpathSync(rootGit)===fs.realpathSync(root),'Command cwd must be monorepo Git root');
 const names=execFileSync('git',['ls-files','-z','--cached','--others','--exclude-standard'],{cwd:root}).toString().split('\0').filter(Boolean);
 const sourceNames=[...new Set(names)].filter(p=>!p.startsWith('docs/')&&!p.startsWith('pdlc-run-')&&!/(^|\/)(node_modules|\.git|\.cache)\//.test(p)).sort();
 const files={};for(const p of sourceNames)files[p]=fs.existsSync(safe(p))?hashFile(p):'deleted';
 const d=folder(i),contracts={};for(const p of [...contractNames.map(n=>d+'/'+n),...listDir(d+'/contracts'),...listDir(d+'/decisions')].sort()){
  contracts[p]=fs.existsSync(safe(p))?hashFile(p):'missing';
 }
 let commit=null;try{commit=execFileSync('git',['rev-parse','HEAD'],{cwd:root,stdio:['ignore','pipe','ignore']}).toString().trim();}catch{}
 return {ok:true,captured_at:new Date().toISOString(),commit,source_hash:sha(JSON.stringify(files)),contract_hash:sha(JSON.stringify(contracts)),files,contracts};
}
export function validateReport(i,p){
 const {e}=validateSpec(i),r=read(p);schemaCheck(r,read('tools/hg/schemas/test-report.schema.json'));
 const start=Date.parse(r.started_at),finish=Date.parse(r.finished_at);
 must(Number.isFinite(start)&&Number.isFinite(finish)&&finish>=start&&finish<=Date.now()+5000,'Invalid report timestamps');
 const cases=unique(r.cases,'executed E2E');
 for(const x of cases.values()){
  must(e.has(x.id),'Unmodelled executed E2E '+x.id);
  must(x.chain.join('|')===e.get(x.id).chain.join('|'),'Unexpected execution chain '+x.id);
  for(const comp of x.chain)must(r.environment.real_components.includes(comp),'Component not real '+comp);
 }
 for(const x of e.values())if(x.required){
  must(cases.has(x.id),'Required E2E missing '+x.id);
  must(cases.get(x.id).status==='passed','Required E2E not passed '+x.id);
  must(cases.get(x.id).attempts===1,'Flaky/retried E2E '+x.id);
 }
 return {r,start,finish};
}
export function validateNfr(i,p){
 const {data}=validateSpec(i),requirements=data.system.nfr;
 if(!requirements.length)return null;
 must(p&&p!=='-','Required NFR report missing');
 const report=read(p);schemaCheck(report,read('tools/hg/schemas/nfr-report.schema.json'));
 const checks=unique(report.checks,'NFR observation');
 const start=Date.parse(report.started_at),finish=Date.parse(report.finished_at);
 must(Number.isFinite(start)&&Number.isFinite(finish)&&finish>=start,'NFR report timestamps');
 for(const n of requirements){
  const o=checks.get(n.id);must(o,'Missing NFR observation '+n.id);
  for(const k of ['metric','unit','conditions','verification'])must(o[k]===n[k],'NFR measurement mismatch '+n.id+'/'+k);
  must(o.status==='passed','NFR not passed '+n.id);
  const passed=n.operator==='<='?o.observed<=n.threshold:n.operator==='>='?o.observed>=n.threshold:o.observed===n.threshold;
  must(passed,'NFR threshold not satisfied '+n.id);
 }
 return {report,start,finish};
}
export function receipt(stage,i,beforePath,out,rc,log,report){
 const problems=[];let before={},after={};
 try{before=read(beforePath);must(before.ok,'Precheck snapshot failed');after=snapshot(i);must(before.source_hash===after.source_hash,'Source changed during command');must(before.contract_hash===after.contract_hash,'Contract changed during command');}catch(e){problems.push(e.message);}
 if(stage==='regression'&&rc===0){try{const z=validateNfr(i,report);if(z)must(z.start>=Date.parse(before.captured_at)-1000,'Stale NFR report');}catch(e){problems.push(e.message);}}
 if(stage==='e2e'&&rc===0){try{const z=validateReport(i,report);must(z.start>=Date.parse(before.captured_at)-1000,'Stale E2E report');}catch(e){problems.push(e.message);}}
 const r={node_id:i.node_id,attempt:i.attempt,stage,passed:rc===0&&!problems.length,exit_code:problems.length&&rc===0?66:rc,started_at:before.captured_at||null,finished_at:new Date().toISOString(),source_hash:after.source_hash||null,contract_hash:after.contract_hash||null,before_source_hash:before.source_hash||null,before_contract_hash:before.contract_hash||null,log_sha256:fs.existsSync(safe(log))?hashFile(log):null,report_sha256:report!=='-'&&fs.existsSync(safe(report))?hashFile(report):null,problems};
 put(out,r);return r;
}
export function validateFinal(i){
 const {d,t,data}=validateSpec(i),now=snapshot(i),r=read(d+'/evidence/e2e-receipt.json'),b=read(d+'/evidence/regression-receipt.json');
 for(const x of [r,b]){
  must(x.passed&&x.exit_code===0,'Evidence command not passed');
  must(x.source_hash===now.source_hash&&x.contract_hash===now.contract_hash,'Evidence stale for current source/contracts');
  must(x.before_source_hash===x.source_hash&&x.before_contract_hash===x.contract_hash,'Mutation during checked command');
 }
 must(b.stage==='regression'&&r.stage==='e2e','Wrong receipt stage');
 if(data.system.nfr.length){must(hashFile(d+'/evidence/nfr-report.json')===b.report_sha256,'NFR report changed');const z=validateNfr(i,d+'/evidence/nfr-report.json');must(z.start>=Date.parse(b.started_at)-1000&&z.finish<=Date.parse(b.finished_at)+1000,'NFR report outside regression window');}
 must(Date.parse(b.finished_at)<=Date.parse(r.started_at),'Regression must precede E2E');
 must(hashFile(d+'/evidence/e2e-report.json')===r.report_sha256,'Saved E2E report modified');
 const logHash=hashFile(d+'/evidence/e2e.log');
 if(logHash!==r.log_sha256){const red=read(d+'/evidence/log-redaction.json');must(red.original_sha256===r.log_sha256&&red.redacted_sha256===logHash&&red.reason,'Unexplained evidence log mutation');}
 const rr=validateReport(i,d+'/evidence/e2e-report.json');
 must(rr.start>=Date.parse(r.started_at)-1000&&rr.finish<=Date.parse(r.finished_at)+1000,'Report outside command time window');
 const impl=read(d+'/implementation.json');
 must(Array.isArray(impl.implemented_tasks),'No task execution record');
 for(const id of t.keys())must(impl.implemented_tasks.includes(id),'Task not implemented '+id);
 must(Array.isArray(impl.files)&&impl.files.some(p=>!/^(docs|tests|tools)\//.test(p)),'No application change');
 for(const p of impl.files)must(fs.existsSync(safe(p)),'Implementation file missing '+p);
 must(read(d+'/change.json').status==='e2e_verified_not_released','Wrong terminal business status');
 const ix=read('docs/product/index.json');must(Array.isArray(ix.changes)&&ix.changes.some(x=>x.change_id===i.change_id),'Product index missing change');
 must(fs.readFileSync(safe(d+'/verification.md'),'utf8').length>100,'Missing useful verification document');
 return {passed:true,source_hash:now.source_hash,contract_hash:now.contract_hash};
}
async function main(){
 const [mode,...args]=process.argv.slice(2);
 if(mode==='receipt'){
  const [stage,ip,before,out,rc,log,report]=args;const r=receipt(stage,input(ip),before,out,Number(rc),log,report);console.log(JSON.stringify({check:stage,passed:r.passed,problems:r.problems}));return;
 }
 const i=input(args[0]);
 if(mode==='snapshot'){
  try{put(args[1],snapshot(i));}catch(e){put(args[1],{ok:false,error:e.message,captured_at:new Date().toISOString()});throw e;}return;
 }
 if(mode==='spec'){validateSpec(i);console.log('PASS schemas, cross-links, task DAG, protected resources and PRD approval');return;}
 if(mode==='e2e'){validateReport(i,args[1]);console.log('PASS required E2E IDs, statuses, attempt counts, declared real chain');return;}
 if(mode==='final'){console.log(JSON.stringify(validateFinal(i)));return;}
 throw new Error('Unknown checker operation; supported: snapshot, spec, e2e, receipt, final');
}
if(process.argv[1]&&pathToFileURL(path.resolve(process.argv[1])).href===import.meta.url){
 main().catch(e=>{console.error('CHECK FAILED: '+e.message);process.exitCode=1;});
}
