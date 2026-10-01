"""Re-crop the v08 hero PNGs by alpha (shadow catcher leaves faint alpha on the whole floor)."""
import bpy, os, json
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mp = os.path.join(ROOT, 'blender', 'metrics-v08.json'); metrics = json.load(open(mp, encoding='utf-8'))
def crop_export(png, outputs, threshold, pad=.05):
    img = bpy.data.images.load(os.path.join(ROOT, 'blender', png)); w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)
    for t in (.01, .05, .1, .2, .35):
        ys, xs = np.where(px[:, :, 3] > t); print('THRESH', png, t, xs.min(), xs.max(), h-1-ys.max(), h-1-ys.min())
    ys, xs = np.where(px[:, :, 3] > threshold)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); p = int(max(x1 - x0, y1 - y0) * pad)
    x0, y0 = max(0, x0 - p), max(0, y0 - p); x1, y1 = min(w - 1, x1 + p), min(h - 1, y1 + p)
    sub = px[y0:y1 + 1, x0:x1 + 1].copy(); ch, cw = sub.shape[:2]
    # Fade residual floor alpha to zero at the crop border so nothing reads as a plate edge.
    yy, xx = np.mgrid[0:ch, 0:cw]; edge = np.minimum.reduce([xx, cw - 1 - xx, yy, ch - 1 - yy]) / (pad * max(cw, ch) + 1)
    sub[:, :, 3] *= np.clip(edge, 0, 1)
    metrics[png + '_frame'] = [int(w), int(h), int(x0), int(h - 1 - y1), int(cw), int(ch)]
    for out, width, quality in outputs:
        c = bpy.data.images.new('crop', cw, ch, alpha=True); c.pixels[:] = sub.ravel(); c.scale(width, round(ch * width / cw))
        path = os.path.join(ROOT, 'assets', out); c.file_format = 'WEBP'; c.save(filepath=path, quality=quality)
        metrics[out] = [width, round(ch * width / cw), os.path.getsize(path)]; bpy.data.images.remove(c)
    bpy.data.images.remove(img)
crop_export('residencia-rincao-v08-desktop.png', [('house-v08-1800.webp', 1800, 84), ('house-v08-1200.webp', 1200, 82)], .35)
crop_export('residencia-rincao-v08-mobile.png', [('house-v08-mobile-900.webp', 900, 82)], .35)
json.dump(metrics, open(mp, 'w', encoding='utf-8'), indent=2); print('CROP_DONE', json.dumps(metrics))
