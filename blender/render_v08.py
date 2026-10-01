"""V08 hero posters: transparent film + shadow catcher floor, so the page owns floor/background.
Starts from residencia-rincao-v07.blend (geometry untouched). Public-render study, approximate.
Also writes responsive WebP variants of the project images (originals untouched).
"""
import bpy, os, time, json
import numpy as np
from mathutils import Vector
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, 'blender', 'residencia-rincao-v07.blend'))
s = bpy.context.scene
metrics = {}

# Floor becomes a shadow catcher: only the contact shadow survives in alpha. No green, no plate edge.
floor = s.objects['Paisagem editorial solo']
floor.is_shadow_catcher = True
s.render.film_transparent = True

# Warm interior light reads through the glass: the single amber accent of the page.
interior = s.objects['V07 interior editorial']
interior.data.energy = 220
interior.data.color = (1, .70, .42)
bpy.ops.object.light_add(type='POINT', location=(-1.6, 3.4, 1.7))
side = bpy.context.object; side.name = 'V08 interior lateral'; side.data.energy = 60; side.data.color = (1, .72, .45); side.data.shadow_soft_size = .6
s.objects['V07 facade daylight'].data.color = (1, .95, .88)
# Light emitters must never appear in glass reflections/transmission as discs.
for o in s.objects:
    if o.type == 'LIGHT':
        o.visible_camera = False; o.visible_glossy = False; o.visible_transmission = False

cam = s.camera
def camera(pos, target, lens):
    cam.location = pos; cam.data.lens = lens
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()

s.render.engine = 'CYCLES'; s.cycles.use_denoising = True
s.render.image_settings.file_format = 'PNG'; s.render.image_settings.color_mode = 'RGBA'
s['v08_notice'] = '2026-10-01: transparent hero posters, shadow catcher floor, warm interior light. Geometry from v07; approximate study.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, 'blender', 'residencia-rincao-v08.blend'))

def render(name, w, h, samples):
    s.render.resolution_x = w; s.render.resolution_y = h; s.render.resolution_percentage = 100; s.cycles.samples = samples
    path = os.path.join(ROOT, 'blender', name); s.render.filepath = path
    t = time.perf_counter(); bpy.ops.render.render(write_still=True); metrics[name + '_seconds'] = round(time.perf_counter() - t, 2)
    return path

def crop_export(png, outputs, pad=.02):
    """Crop to the alpha bounding box (with padding) and export WebP sizes."""
    img = bpy.data.images.load(png); w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)
    ys, xs = np.where(px[:, :, 3] > .01)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    p = int(max(x1 - x0, y1 - y0) * pad)
    x0, y0 = max(0, x0 - p), max(0, y0 - p); x1, y1 = min(w - 1, x1 + p), min(h - 1, y1 + p)
    sub = px[y0:y1 + 1, x0:x1 + 1].copy(); ch, cw = sub.shape[:2]
    metrics[os.path.basename(png) + '_frame'] = [int(w), int(h), int(x0), int(h - 1 - y1), int(cw), int(ch)]  # w,h,x0,y0(top),cw,ch
    for out, width, quality in outputs:
        c = bpy.data.images.new('crop', cw, ch, alpha=True); c.pixels[:] = sub.ravel()
        c.scale(width, round(ch * width / cw))
        c.filepath_raw = os.path.join(ROOT, 'assets', out); c.file_format = 'WEBP'
        s.render.image_settings.quality = quality
        c.save(filepath=c.filepath_raw, quality=quality)
        metrics[out] = [width, round(ch * width / cw), os.path.getsize(c.filepath_raw)]
        bpy.data.images.remove(c)
    bpy.data.images.remove(img)

camera((-12.6, 25.8, 3.7), (-.7, 1.0, 1.55), 46)
desk = render('residencia-rincao-v08-desktop.png', 2400, 1500, 96)
crop_export(desk, [('house-v08-1800.webp', 1800, 84), ('house-v08-1200.webp', 1200, 82)])
camera((-8.4, 24.8, 3.9), (-.7, 1.2, 1.6), 44)
mob = render('residencia-rincao-v08-mobile.png', 1400, 1400, 64)
crop_export(mob, [('house-v08-mobile-900.webp', 900, 82)])

# Responsive project images (originals preserved).
for name in ['loft-arquitetura', 'projeto-estrutural', 'residencia-em-construcao']:
    img = bpy.data.images.load(os.path.join(ROOT, 'assets', name + '.webp')); w, h = img.size
    for width in (800,):
        c = img.copy(); c.scale(width, round(h * width / w))
        out = os.path.join(ROOT, 'assets', '%s-%d.webp' % (name, width)); c.file_format = 'WEBP'; c.save(filepath=out, quality=80)
        metrics['%s-%d.webp' % (name, width)] = [width, round(h * width / w), os.path.getsize(out)]
        bpy.data.images.remove(c)
    bpy.data.images.remove(img)

with open(os.path.join(ROOT, 'blender', 'metrics-v08.json'), 'w', encoding='utf-8') as f:
    json.dump(metrics, f, indent=2)
print('V08_COMPLETE', json.dumps(metrics))
