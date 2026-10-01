"""Encode untouched Blender-render pixels and compose QA/reference proofs.
No retouching of reference images or fabrication of client photography.
"""
from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
data=json.loads((ROOT/'blender/metrics-v07.json').read_text(encoding='utf-8'))
data.pop('mobile_second_pass_render_seconds',None)
data['mobile_second_pass_timing_notice']='Blender log saved at46.891s including2.282s scene load; exact perf_counter result overwritten by concurrent packaging, not used as performance claim.'
data['glb_final_meshes']=22;data['glb_final_triangles']=58871;data['glb_embedded_webp_texture_bytes']=5502
for suffix in ['desktop','mobile']:
 source=ROOT/'blender'/f'residencia-rincao-v07-{suffix}.png'
 asset=ROOT/'assets'/f'house-v07-{suffix}.webp'
 Image.open(source).save(asset,'WEBP',quality=92,method=6)
 data[f'poster_{suffix}_bytes']=asset.stat().st_size
total=0
for source in sorted((ROOT/'blender/sequence-v07').glob('phase-*.png')):
 dest=source.with_suffix('.webp');Image.open(source).save(dest,'WEBP',quality=88,method=6);total+=dest.stat().st_size
data['sequence_prototype_7_frames_webp_bytes']=total
data['sequence_prototype_dimensions']='640x400'
data['sequence_prototype_notice']='7 phase snapshots only; not an equivalent continuous 30/60fps production sequence or FPS measurement.'
sheet=Image.new('RGB',(2400,1080),'#111112');d=ImageDraw.Draw(sheet)
title=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',30);body=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
d.text((40,25),'RENDER OFICIAL — DELLA & PUCKER',font=title,fill='white')
d.text((1240,25),'BLENDER V07 — ESTUDO APROXIMADO',font=title,fill='white')
for path,x in [(ROOT/'references/render-perspectiva.webp',40),(ROOT/'blender/residencia-rincao-v07-desktop.png',1240)]:
 im=Image.open(path).convert('RGBA')
 if x==1240:im=im.crop((170,180,1460,840)) # QA only: compare architecture at equivalent visual scale.
 im=ImageOps.contain(im,(1120,850),Image.Resampling.LANCZOS)
 sheet.paste(im,(x,100+(850-im.height)//2),im)
d.text((40,1000),'Referência publicada é render, não fotografia. Original preservado.',font=body,fill='#bdbdc2')
d.text((1240,1000),'Câmera/iluminação/piso editoriais; medidas e partes ocultas aproximadas.',font=body,fill='#bdbdc2')
sheet.save(ROOT/'blender/comparacao-v07-referencia.png',optimize=True)
phases=Image.new('RGB',(1600,920),'#111112');d=ImageDraw.Draw(phases)
for i,path in enumerate(sorted((ROOT/'blender/sequence-v07').glob('phase-*.png'))):
 im=ImageOps.contain(Image.open(path).convert('RGBA'),(380,340),Image.Resampling.LANCZOS)
 x=(i%4)*400+10;y=(i//4)*440+50;phases.paste(im,(x,y),im)
 d.text((x,(i//4)*440+20),f'Fase {i}: estudo construtivo',font=body,fill='white')
phases.save(ROOT/'blender/comparacao-v07-fases.jpg',quality=92)
(ROOT/'blender/metrics-v07.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(data,indent=2,ensure_ascii=False))
