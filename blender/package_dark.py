"""Package Blender output without retouching reference photographs or renders."""
from PIL import Image, ImageOps, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
for suffix,asset in [('dark','house-dark.webp'),('dark-mobile','house-dark-mobile.webp')]:
    Image.open(ROOT/'blender'/f'residencia-rincao-{suffix}.png').save(ROOT/'assets'/asset,'WEBP',quality=94,method=6)
sheet=Image.new('RGB',(2400,1050),'#171719');d=ImageDraw.Draw(sheet)
title=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',30)
body=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
d.text((40,30),'RENDER OFICIAL — DELLA & PUCKER',font=title,fill='white')
d.text((1240,30),'BLENDER — ESTUDO VISUAL APROXIMADO',font=title,fill='white')
for path,x in [(ROOT/'references/render-perspectiva.webp',40),(ROOT/'blender/residencia-rincao-dark.png',1240)]:
    im=Image.open(path).convert('RGBA');im=ImageOps.contain(im,(1120,840),Image.Resampling.LANCZOS)
    sheet.paste(im,(x,110+(840-im.height)//2),im)
d.text((40,995),'Instagram oficial · DXfLBPXj5nQ · referência é render, não fotografia.',font=body,fill='#c6c6ca')
d.text((1240,995),'Medidas e partes ocultas aproximadas. Iluminação editorial.',font=body,fill='#c6c6ca')
sheet.save(ROOT/'blender/comparacao-dark-referencia.png',optimize=True)
print('Posters e comparação escura gerados.')
