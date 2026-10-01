import { cp, mkdir, rm } from 'node:fs/promises';
import { resolve, basename } from 'node:path';
import { buildScene } from './scene-build.mjs';

const root = resolve(import.meta.dirname, '..');
const out = resolve(root, 'dist');
// Legacy posters/models and Blender texture sources stay in the repo but are not served.
const legacy = new Set(['house-dark.webp', 'house-dark-mobile.webp', 'house-final.webp', 'house-mobile.webp', 'house-v07-desktop.webp', 'house-v07-mobile.webp', 'residencia-rincao.glb', 'textures']);
await buildScene();
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const entry of ['index.html', 'style.css']) await cp(resolve(root, entry), resolve(out, entry));
await cp(resolve(root, 'assets'), resolve(out, 'assets'), { recursive: true, filter: src => !legacy.has(basename(src)) });
await mkdir(resolve(out, 'references'), { recursive: true });
await cp(resolve(root, 'references/planta-referencia.webp'), resolve(out, 'references/planta-referencia.webp'));
console.log('Prévia estática pronta em ' + out);
