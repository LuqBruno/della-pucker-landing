"""Internal comparison sheet; user inspiration is never copied into the website."""
from PIL import Image, ImageOps, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sheet=Image.new('RGB',(2600,1670),'#19191b');d=ImageDraw.Draw(sheet)
title=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',38)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',27)
d.text((45,25),'REFERÊNCIAS DE COMPOSIÇÃO',font=title,fill='white')
d.text((1040,25),'DELLA & PUCKER — PRÉVIA LOCAL 0.5.0',font=title,fill='white')
def place(im,box):
    im=ImageOps.contain(im.convert('RGB'),(box[2],box[3]),Image.Resampling.LANCZOS)
    sheet.paste(im,(box[0]+(box[2]-im.width)//2,box[1]+(box[3]-im.height)//2))
hotle=Image.open('C:/Users/itzlu/Downloads/Modern Web Design Ideas_ Clean, Industrial Style.jpg')
place(hotle.crop((hotle.width*.07,hotle.height*.045,hotle.width*.93,hotle.height*.475)),(45,90,920,740))
d.text((45,845),'Hotle: escala, casa/tipografia e profundidade.',font=small,fill='#c5c5ca')
kontra=Image.open('C:/Users/itzlu/Downloads/12b54b43360f7115552ddb05680390e7.jpg')
place(kontra.crop((0,0,kontra.width,kontra.height*.264)),(45,925,920,550))
d.text((45,1520),'Kontra: contraste e presença arquitetônica.',font=small,fill='#c5c5ca')
place(Image.open(ROOT/'docs/qa/qa-v05-hero-1440.jpg'),(1040,90,1515,947))
place(Image.open(ROOT/'docs/qa/qa-v05-hero-375.jpg'),(1040,1080,260,555))
for i,line in enumerate(['Preto/grafite orientado pela logo real.', 'Casa oficial reconstruída como estudo aproximado.', 'CTA imediato; construção responde ao scroll.', 'Composição adaptada ao celular, não comprimida.', 'Referências inspiram princípios, não a identidade.', 'Paisagem e luz não são reprodução do render oficial.']):
    d.text((1350,1140+i*58),line,font=small,fill='#d5d5d8')
sheet.save(ROOT/'docs/qa/comparacao-direcao-v05.png',optimize=True)
print('Comparação de composição salva.')
