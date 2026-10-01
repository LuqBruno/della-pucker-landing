import { cp, mkdir, rm } from 'node:fs/promises';
import { resolve } from 'node:path';
import { buildScene } from './scene-build.mjs';

const root = resolve(import.meta.dirname, '..');
const out = resolve(root, 'dist');
await buildScene();
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const entry of ['index.html', 'style.css', 'dark.css', 'script.js', 'gallery.js', 'assets']) {
  await cp(resolve(root, entry), resolve(out, entry), { recursive: true });
}
await mkdir(resolve(out,'references'),{recursive:true});
await cp(resolve(root,'references/planta-referencia.webp'),resolve(out,'references/planta-referencia.webp'));
console.log('Prévia estática pronta em ' + out);
