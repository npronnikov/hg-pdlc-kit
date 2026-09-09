import http from 'node:http';
import {DatabaseSync} from 'node:sqlite';
if(process.env.DEMO_MODE!=='1')throw new Error('Educational fixture only');
const tokens=JSON.parse(process.env.TEST_TOKENS_JSON||'{}');
const db=new DatabaseSync(process.env.DB_PATH||':memory:');
db.exec('CREATE TABLE IF NOT EXISTS tickets(id TEXT PRIMARY KEY,title TEXT NOT NULL,owner TEXT NOT NULL)');
const server=http.createServer((req,res)=>{
 const m=/^\/api\/tickets\/([a-zA-Z0-9-]+)$/.exec(req.url);
 const token=String(req.headers.authorization||'').replace(/^Bearer /,'');
 const owner=Object.hasOwn(tokens,token)?tokens[token]:null;
 let status=404,body={error:'not_found'};
 if(req.url==='/health'){status=200;body={status:'ok'};}
 else if(!owner){status=401;body={error:'unauthorized'};}
 else if(m&&req.method==='GET'){const row=db.prepare('SELECT id,title FROM tickets WHERE id=? AND owner=?').get(m[1],owner);if(row){status=200;body=row;}}
 res.writeHead(status,{'content-type':'application/json'});res.end(JSON.stringify(body));
});
server.listen(Number(process.env.PORT||0),'127.0.0.1',()=>console.log('READY '+server.address().port));
process.on('SIGTERM',()=>server.close(()=>{db.close();process.exit(0);}));
