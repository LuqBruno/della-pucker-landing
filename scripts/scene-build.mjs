import { build } from 'esbuild';
import { resolve } from 'node:path';
export async function buildScene() {
  const root = resolve(import.meta.dirname, '..');
  await build({entryPoints:[resolve(root,'scene/house-scene.js')],bundle:true,minify:true,format:'esm',target:'es2022',outfile:resolve(root,'assets/house-scene.js'),legalComments:'eof'});
  await build({entryPoints:[resolve(root,'script.js')],bundle:true,minify:true,format:'esm',target:'es2022',outfile:resolve(root,'assets/site.js'),legalComments:'eof'});
}
if (process.argv[1]?.endsWith('scene-build.mjs')) await buildScene();
