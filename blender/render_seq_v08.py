"""Mobile construction sequence (no WebGL on phones): 7 transparent frames on the mobile poster camera.
Frame 0 = project lines only (Freestyle over holdout); 1-5 = cumulative build stages; 6 = the mobile poster itself.
Same crop rectangle as house-v08-mobile-900.webp, so frames stack exactly over the poster.
"""
import bpy, os, json, time
import numpy as np
from mathutils import Vector
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, 'blender', 'residencia-rincao-v08.blend'))
s = bpy.context.scene; vl = bpy.context.view_layer
mp = os.path.join(ROOT, 'blender', 'metrics-v08.json'); metrics = json.load(open(mp, encoding='utf-8'))
W, H, X0, Y0, CW, CH = metrics['residencia-rincao-v08-mobile.png_frame']
cam = s.camera; cam.location = (-8.4, 24.8, 3.9); cam.data.lens = 44
cam.rotation_euler = (Vector((-.7, 1.2, 1.6)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
s.render.engine = 'CYCLES'; s.cycles.use_denoising = True; s.cycles.samples = 32
s.render.resolution_x = W; s.render.resolution_y = H; s.render.resolution_percentage = 100
s.render.film_transparent = True; s.render.image_settings.file_format = 'PNG'; s.render.image_settings.color_mode = 'RGBA'
meshes = [o for o in s.objects if o.type == 'MESH' and 'buildStage' in o and o.name != 'Paisagem editorial solo']
os.makedirs(os.path.join(ROOT, 'assets', 'build-seq'), exist_ok=True)
pad = .05

def export(png, out):
    img = bpy.data.images.load(png); px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)
    y_bottom = H - Y0 - CH  # Blender rows start at the bottom
    sub = px[y_bottom:y_bottom + CH, X0:X0 + CW].copy()
    yy, xx = np.mgrid[0:CH, 0:CW]; edge = np.minimum.reduce([xx, CW - 1 - xx, yy, CH - 1 - yy]) / (pad * max(CW, CH) + 1)
    sub[:, :, 3] *= np.clip(edge, 0, 1)
    c = bpy.data.images.new('seq', CW, CH, alpha=True); c.pixels[:] = sub.ravel(); c.scale(900, round(CH * 900 / CW))
    path = os.path.join(ROOT, 'assets', 'build-seq', out); c.file_format = 'WEBP'; c.save(filepath=path, quality=80)
    metrics['build-seq/' + out] = os.path.getsize(path); bpy.data.images.remove(c); bpy.data.images.remove(img)

def render(name):
    path = os.path.join(ROOT, 'blender', 'sequence-v08', name); s.render.filepath = path
    t = time.perf_counter(); bpy.ops.render.render(write_still=True); metrics['seq_' + name + '_seconds'] = round(time.perf_counter() - t, 2)
    return path

# Frame 0: white project lines of the whole house, no solids, no shadow.
holdout = bpy.data.materials.new('V08 holdout'); holdout.use_nodes = True; nt = holdout.node_tree; nt.nodes.clear()
nt.links.new(nt.nodes.new('ShaderNodeHoldout').outputs[0], nt.nodes.new('ShaderNodeOutputMaterial').inputs['Surface'])
vl.material_override = holdout
s.render.use_freestyle = True; s.render.line_thickness_mode = 'ABSOLUTE'; s.render.line_thickness = 1.3
fs = vl.freestyle_settings; fs.crease_angle = 2.4
ls = fs.linesets[0] if fs.linesets else fs.linesets.new('Projeto')
ls.select_by_visibility = True; ls.select_by_edge_types = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
ls.linestyle.color = (.95, .94, .91); ls.linestyle.alpha = .85; ls.linestyle.thickness = 1.3
floor = s.objects['Paisagem editorial solo']; floor.hide_render = True  # its far edge would draw a horizon line
for o in meshes: o.hide_render = int(o['buildStage']) >= 6
export(render('phase-00.png'), 'm-0.webp')
floor.hide_render = False; vl.material_override = None; s.render.use_freestyle = False
import sys
for stage in ([] if '--only0' in sys.argv else range(1, 6)):
    for o in meshes: o.hide_render = int(o['buildStage']) > stage
    export(render('phase-%02d.png' % stage), 'm-%d.webp' % stage)
for o in meshes: o.hide_render = False
json.dump(metrics, open(mp, 'w', encoding='utf-8'), indent=2); print('SEQ_DONE', json.dumps({k: v for k, v in metrics.items() if 'seq' in k}))
