/** Product E2E test harness. Exercises real HTTP, a separate app process, and on-disk SQLite. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawn} from 'node:child_process';
import {DatabaseSync} from 'node:sqlite';
const output=process.argv[2]||'pdlc-run-e2e-report.json';
const chain=['External HTTP client','Ticket API','SQLite'];
const report={runner:'node-assert-http-e2e',started_at:new Date().toISOString(),finished_at:'',environment:{kind:'isolated-local',real_components:chain,external_simulators:[]},cases:[]};
async function start(dbPath){
 const child=spawn(process.execPath,['apps/api/server.mjs'],{cwd:process.cwd(),env:{...process.env,DEMO_MODE:'1',PORT:'0',DB_PATH:dbPath,TEST_TOKENS_JSON:JSON.stringify({'alice-test':'alice','bob-test':'bob'})},stdio:['ignore','pipe','pipe']});
 let stderr='';child.stderr.on('data',x=>stderr+=x);
 let base;
 try{
  base=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>{child.kill('SIGKILL');reject(new Error('readiness timeout: '+stderr));},6000);
   let text='';child.stdout.on('data',chunk=>{text+=chunk;const m=/READY (\d+)/.exec(text);if(m){clearTimeout(timer);resolve('http://127.0.0.1:'+m[1]);}});
   child.once('error',e=>{clearTimeout(timer);reject(e);});
   child.once('exit',code=>{clearTimeout(timer);reject(new Error('server exited '+code+' '+stderr));});
  });
  const r=await fetch(base+'/health',{signal:AbortSignal.timeout(2000)});assert.equal(r.status,200);
 }catch(e){child.kill('SIGKILL');throw e;}
 return {base,async stop(){
  if(child.exitCode!==null)return;
  await new Promise(resolve=>{const t=setTimeout(()=>child.kill('SIGKILL'),3500);child.once('exit',()=>{clearTimeout(t);resolve();});child.kill('SIGTERM');});
 }};
}
async function fixture(fn){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'ticket-e2e-'));const dbPath=path.join(dir,'tickets.sqlite');
 // The legacy fixture deliberately has no priority/version columns. The real application migrates it.
 const db=new DatabaseSync(dbPath);db.exec('CREATE TABLE tickets (id TEXT PRIMARY KEY,title TEXT NOT NULL,owner TEXT NOT NULL)');
 const ins=db.prepare('INSERT INTO tickets(id,title,owner) VALUES (?,?,?)');ins.run('t-alice','Alice ticket','alice');ins.run('t-bob','Bob ticket','bob');db.close();
 let app;
 try{app=await start(dbPath);await fn({get app(){return app;},async restart(){await app.stop();app=await start(dbPath);}});}
 finally{if(app)await app.stop();fs.rmSync(dir,{recursive:true,force:true});}
}
async function req(app,method,id,token='alice-test',payload,raw=false){
 const headers={};if(token)headers.authorization='Bearer '+token;if(payload!==undefined)headers['content-type']='application/json';
 const r=await fetch(app.base+'/api/tickets/'+id+(method==='PATCH'?'/priority':''),{method,headers,body:payload===undefined?undefined:raw?payload:JSON.stringify(payload),signal:AbortSignal.timeout(3000)});
 return {status:r.status,body:await r.json()};
}
async function run(id,assertions,fn){
 const startTime=Date.now();let status='passed';
 try{await fixture(fn);console.log(id+' passed');}catch(e){status='failed';console.error(id+' failed: '+e.stack);process.exitCode=1;}
 report.cases.push({id,status,attempts:1,duration_ms:Date.now()-startTime,assertions,chain});
}
try{
 await run('E2E-001',['Owner PATCH returns 200/high/version=2','Subsequent GET returns persisted high'],async f=>{
  const r=await req(f.app,'PATCH','t-alice','alice-test',{priority:'high',expectedVersion:1});assert.equal(r.status,200);assert.equal(r.body.priority,'high');assert.equal(r.body.version,2);
  const x=await req(f.app,'GET','t-alice');assert.equal(x.body.priority,'high');assert.equal(x.body.version,2);
 });
 await run('E2E-002',['Priority survives application process restart with same on-disk DB'],async f=>{
  assert.equal((await req(f.app,'PATCH','t-alice','alice-test',{priority:'low',expectedVersion:1})).status,200);await f.restart();
  const r=await req(f.app,'GET','t-alice');assert.equal(r.status,200);assert.equal(r.body.priority,'low');assert.equal(r.body.version,2);
 });
 await run('E2E-003',['Other owner GET/PATCH return 404 without object disclosure','Owner reads unchanged data afterwards'],async f=>{
  assert.equal((await req(f.app,'GET','t-alice','bob-test')).status,404);
  const r=await req(f.app,'PATCH','t-alice','bob-test',{priority:'high',expectedVersion:1});assert.equal(r.status,404);assert.deepEqual(r.body,{error:'not_found'});
  const x=await req(f.app,'GET','t-alice');assert.equal(x.body.priority,'normal');assert.equal(x.body.version,1);
 });
 await run('E2E-004',['Missing and invalid tokens return 401','Unauthorized requests do not mutate data'],async f=>{
  for(const token of ['', 'invalid-test'])assert.equal((await req(f.app,'PATCH','t-alice',token,{priority:'high',expectedVersion:1})).status,401);
  assert.equal((await req(f.app,'GET','t-alice')).body.version,1);
 });
 await run('E2E-005',['Unknown enum returns 400','Rejected request preserves priority and version'],async f=>{
  const r=await req(f.app,'PATCH','t-alice','alice-test',{priority:'urgent',expectedVersion:1});assert.equal(r.status,400);assert.equal(r.body.error,'invalid_priority');
  const x=await req(f.app,'GET','t-alice');assert.equal(x.body.priority,'normal');assert.equal(x.body.version,1);
 });
 await run('E2E-006',['Malformed JSON, missing/invalid version and extra fields are rejected with 400','Invalid inputs leave record unchanged','Wrong content type returns 415; oversize body returns 413'],async f=>{
  assert.equal((await req(f.app,'PATCH','t-alice','alice-test','{broken',true)).status,400);
  for(const p of [{priority:'high'},{priority:'high',expectedVersion:0},{priority:'high',expectedVersion:1.2},{priority:'high',expectedVersion:1,owner:'bob'}])assert.equal((await req(f.app,'PATCH','t-alice','alice-test',p)).status,400);
  const badType=await fetch(f.app.base+'/api/tickets/t-alice/priority',{method:'PATCH',headers:{authorization:'Bearer alice-test','content-type':'text/plain'},body:'{}',signal:AbortSignal.timeout(3000)});assert.equal(badType.status,415);
  assert.equal((await req(f.app,'PATCH','t-alice','alice-test','x'.repeat(9000),true)).status,413);
  assert.equal((await req(f.app,'GET','t-alice')).body.version,1);
 });
 await run('E2E-007',['Concurrent requests with same version produce exactly one 200 and one 409','Winner persists and version increments only once'],async f=>{
  const rs=await Promise.all(['high','low'].map(priority=>req(f.app,'PATCH','t-alice','alice-test',{priority,expectedVersion:1})));
  assert.deepEqual(rs.map(r=>r.status).sort(),[200,409]);
  const r=await req(f.app,'GET','t-alice');assert.equal(r.body.version,2);assert.equal(r.body.priority,rs.find(x=>x.status===200).body.priority);
 });
 await run('E2E-008',['Legacy table migrates preserving id/title','Existing records have default normal/version=1'],async f=>{
  const r=await req(f.app,'GET','t-alice');assert.equal(r.status,200);assert.deepEqual(r.body,{id:'t-alice',title:'Alice ticket',priority:'normal',version:1});
 });
 await run('E2E-009',['Missing object returns same 404 error as inaccessible object','No existing ticket is changed'],async f=>{
  const r=await req(f.app,'PATCH','missing','alice-test',{priority:'high',expectedVersion:1});assert.equal(r.status,404);assert.deepEqual(r.body,{error:'not_found'});
  assert.equal((await req(f.app,'GET','t-alice')).body.version,1);
 });
}finally{
 report.finished_at=new Date().toISOString();fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
}
