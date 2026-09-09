import http from 'node:http';
import {DatabaseSync} from 'node:sqlite';
import {parsePriority} from './priority.mjs';
if(process.env.DEMO_MODE!=='1')throw new Error('This is an educational fixture, not production authentication');
const tokens=JSON.parse(process.env.TEST_TOKENS_JSON||'{}');
if(Object.keys(tokens).length===0)throw new Error('Isolated test tokens are required');
const db=new DatabaseSync(process.env.DB_PATH||':memory:');
db.exec('PRAGMA busy_timeout=5000; CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY,title TEXT NOT NULL,owner TEXT NOT NULL)');
// Brownfield-safe additive migration; existing id/title/owner data are preserved.
const columns=db.prepare('PRAGMA table_info(tickets)').all().map(x=>x.name);
if(!columns.includes('priority'))db.exec("ALTER TABLE tickets ADD COLUMN priority TEXT NOT NULL DEFAULT 'normal' CHECK(priority IN ('low','normal','high'))");
if(!columns.includes('version'))db.exec('ALTER TABLE tickets ADD COLUMN version INTEGER NOT NULL DEFAULT 1 CHECK(version >= 1)');
const owned=db.prepare('SELECT id,title,priority,version FROM tickets WHERE id=? AND owner=?');
const update=db.prepare('UPDATE tickets SET priority=?,version=version+1 WHERE id=? AND owner=? AND version=? RETURNING id,title,priority,version');
function send(res,status,body){res.writeHead(status,{'content-type':'application/json; charset=utf-8','cache-control':'no-store'});res.end(JSON.stringify(body));}
async function body(req){
 let n=0;const parts=[];let tooLarge=false;
 for await(const chunk of req){n+=chunk.length;if(n>8192){tooLarge=true;continue;}parts.push(chunk);}
 if(tooLarge){const e=new Error('body_too_large');e.status=413;throw e;}
 try{return JSON.parse(Buffer.concat(parts).toString('utf8'));}catch{throw new Error('invalid_json');}
}
const server=http.createServer(async(req,res)=>{
 try{
  const u=new URL(req.url,'http://127.0.0.1');
  if(req.method==='GET'&&u.pathname==='/health'){send(res,200,{status:'ok'});return;}
  const m=/^\/api\/tickets\/([a-zA-Z0-9-]+)(\/priority)?$/.exec(u.pathname);
  if(!m){send(res,404,{error:'not_found'});return;}
  const auth=req.headers.authorization||'';
  const token=auth.startsWith('Bearer ')?auth.slice(7):'';
  const owner=Object.hasOwn(tokens,token)?tokens[token]:null;
  if(!owner){send(res,401,{error:'unauthorized'});return;}
  const ticket=owned.get(m[1],owner);
  if(!ticket){send(res,404,{error:'not_found'});return;}
  if(req.method==='GET'&&!m[2]){send(res,200,ticket);return;}
  if(req.method==='PATCH'&&m[2]){
   if(!String(req.headers['content-type']||'').startsWith('application/json')){send(res,415,{error:'json_required'});return;}
   let change;
   try{change=parsePriority(await body(req));}catch(e){send(res,e.status||400,{error:e.message});return;}
   const changed=update.get(change.priority,m[1],owner,change.expectedVersion);
   if(!changed){send(res,409,{error:'version_conflict'});return;}
   send(res,200,changed);return;
  }
  send(res,405,{error:'method_not_allowed'});
 }catch(e){console.error('request_failed',e.name);if(!res.headersSent)send(res,500,{error:'internal_error'});else res.end();}
});
server.requestTimeout=10000;server.headersTimeout=5000;
server.listen(Number(process.env.PORT||0),'127.0.0.1',()=>console.log('READY '+server.address().port));
let stopping=false;
function stop(){if(stopping)return;stopping=true;server.close(()=>{db.close();process.exit(0);});setTimeout(()=>process.exit(1),3000).unref();}
process.on('SIGTERM',stop);process.on('SIGINT',stop);
