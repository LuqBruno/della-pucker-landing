"""Package unchanged Blender render pixels into a web poster and visual QA sheet."""
from PIL import Image,ImageDraw,ImageFont,ImageOps
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=ROOT/'blender'/'residencia-rincao-final.png'
im=Image.open(source).convert('RGBA')
bbox=im.getchannel('A').getbbox()
if bbox:
    x0,y0,x1,y1=bbox;pad=35
    poster=im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
else:poster=im
# Keep the camera's sky margin in the deployed fallback; cropping alpha would
# cut the roof when the responsive image uses cover on a wide hero.
im.save(ROOT/'assets'/'house-final.webp',format='WEBP',quality=94,method=6)
mobile=ROOT/'blender'/'residencia-rincao-mobile.png'
if mobile.exists():Image.open(mobile).save(ROOT/'assets'/'house-mobile.webp',format='WEBP',quality=94,method=6)
W,H=2800,1170
canvas=Image.new('RGB',(W,H),'#f2f2ef');draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',38)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
draw.text((65,35),'REFERÊNCIA PUBLICADA — DELLA & PUCKER',font=font,fill='#242824')
draw.text((1465,35),'MODELO NO BLENDER — ESTUDO APROXIMADO',font=font,fill='#242824')
ref=Image.open(ROOT/'references'/'render-perspectiva.webp').convert('RGB')
ref=ImageOps.contain(ref,(1300,960),Image.Resampling.LANCZOS)
canvas.paste(ref,(65,110+(960-ref.height)//2))
mod=ImageOps.contain(poster,(1270,960),Image.Resampling.LANCZOS)
canvas.paste(mod,(1470,110+(960-mod.height)//2),mod)
draw.line((1400,105,1400,1070),fill='#c5c8c2',width=2)
draw.text((65,1090),'Render público: instagram.com/dellapucker/p/DXfLBPXj5nQ/',font=small,fill='#575c57')
draw.text((1465,1090),'Proporções estimadas. Estrutura oculta ilustrativa. Sem precisão executiva.',font=small,fill='#575c57')
canvas.save(ROOT/'blender'/'comparacao-referencia-modelo.png',optimize=True)
print('POSTER',poster.size,(ROOT/'assets'/'house-final.webp').stat().st_size)
