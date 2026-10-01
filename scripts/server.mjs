import { createServer } from 'node:http';
import { readFile, stat, writeFile, mkdir } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const port = Number(process.env.PORT || 3012);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png':'image/png', '.jpg':'image/jpeg' };

createServer(async (req, res) => {
  try {
    // Development-only capture endpoint. Fixed image targets and loopback access.
    const requestUrl=new URL(req.url,'http://localhost');
    if(req.method==='POST'&&requestUrl.pathname==='/__capture'){
      const allowed=['127.0.0.1','::1','::ffff:127.0.0.1'].includes(req.socket.remoteAddress);
      const name=requestUrl.searchParams.get('name')||'';
      if(!allowed||!(/^(house-final\.webp|qa-[a-z0-9-]+\.jpg)$/.test(name)))throw new Error('Invalid capture');
      const chunks=[];let total=0;
      for await(const chunk of req){total+=chunk.length;if(total>8*1024*1024)throw new Error('Capture too large');chunks.push(chunk);}
      const folder=resolve(root,name==='house-final.webp'?'assets':'docs/qa');await mkdir(folder,{recursive:true});await writeFile(resolve(folder,name),Buffer.concat(chunks));
      res.writeHead(200,{'Content-Type':'text/plain; charset=utf-8'});res.end('Captura salva: '+name);return;
    }
    const path = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    const file = resolve(root, '.' + (path === '/' ? '/index.html' : path));
    if (file !== root && !file.startsWith(root + sep)) throw new Error('Outside root');
    const info = await stat(file);
    if (!info.isFile()) throw new Error('Not a file');
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(await readFile(file));
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Não encontrado');
  }
}).listen(port, () => console.log('Della & Pucker: http://localhost:' + port));
