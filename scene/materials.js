import * as THREE from 'three';

// Deterministic, local textures: dimensions in the model are expressed in metres.
export function random(seed = 46) {
  return () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
}
function canvas(size, paint, colorSpace = THREE.SRGBColorSpace) {
  const el = document.createElement('canvas'); el.width = el.height = size;
  paint(el.getContext('2d'), size);
  const texture = new THREE.CanvasTexture(el);
  texture.colorSpace = colorSpace;
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.anisotropy = 4;
  return texture;
}
export function createMaterials(lowPower) {
  const size = lowPower ? 256 : 512;
  const grain = (base, spread, seed) => canvas(size, (ctx,n) => {
    const rng=random(seed), data=ctx.createImageData(n,n);
    for(let i=0;i<data.data.length;i+=4){const k=(rng()-.5)*spread; for(let c=0;c<3;c++)data.data[i+c]=base[c]+k; data.data[i+3]=255;}
    ctx.putImageData(data,0,0);
    ctx.globalAlpha=.07; ctx.strokeStyle='#625e56'; ctx.lineWidth=1;
    for(let i=0;i<22;i++){const x=rng()*n,y=rng()*n;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+12+rng()*50,y+rng()*5);ctx.stroke();}
  });
  const concrete=grain([179,179,170],30,7); concrete.repeat.set(3,3);
  const plaster=grain([230,227,218],14,18); plaster.repeat.set(2,2);
  const sand=grain([186,173,151],28,13); sand.repeat.set(5,5);
  const lawn=grain([110,122,80],40,20); lawn.repeat.set(8,8);
  const gravel=canvas(size,(ctx,n)=>{ctx.fillStyle='#b2b0a5';ctx.fillRect(0,0,n,n);const rng=random(8);for(let i=0;i<9000;i++){const shade=120+Math.floor(rng()*80);ctx.fillStyle=`rgb(${shade},${shade},${shade-8})`;ctx.beginPath();ctx.ellipse(rng()*n,rng()*n,1+rng()*2,.5+rng()*2,rng()*Math.PI,0,Math.PI*2);ctx.fill();}});gravel.repeat.set(4,4);
  const wood=canvas(size,(ctx,n)=>{ctx.fillStyle='#997150';ctx.fillRect(0,0,n,n);const rng=random(12);for(let i=0;i<700;i++){ctx.globalAlpha=.03+rng()*.2;ctx.strokeStyle=rng()>.5?'#3e2c20':'#d2ab79';ctx.lineWidth=.4+rng()*1.5;const x=rng()*n;ctx.beginPath();ctx.moveTo(x,0);ctx.bezierCurveTo(x+rng()*9,n*.35,x-rng()*8,n*.65,x,n);ctx.stroke();}});
  const brick=canvas(size,(ctx,n)=>{ctx.fillStyle='#c1b5a1';ctx.fillRect(0,0,n,n);const rng=random(5);const h=n/8,w=n/4;for(let y=0;y<8;y++)for(let x=-1;x<5;x++){const shade=150+Math.floor(rng()*28);ctx.fillStyle=`rgb(${shade+28},${shade+15},${shade})`;ctx.fillRect(x*w+(y%2?w/2:0)+2,y*h+2,w-4,h-4);}});brick.repeat.set(2,2);
  const mat=(options)=>new THREE.MeshStandardMaterial(options);
  return {
    concrete:mat({map:concrete,color:'#bbb9ae',bumpMap:concrete,bumpScale:.025,roughness:.88}),
    plaster:mat({map:plaster,color:'#e3e0d6',bumpMap:plaster,bumpScale:.008,roughness:.94}),
    masonry:mat({map:brick,bumpMap:brick,bumpScale:.028,roughness:.92}),
    stone:mat({map:sand,color:'#c3b9a6',bumpMap:sand,bumpScale:.035,roughness:.9}),
    ground:mat({map:sand,color:'#d4c8b2',roughness:1}),
    lawn:mat({map:lawn,color:'#8f9c79',bumpMap:lawn,bumpScale:.025,roughness:1}),
    gravel:mat({map:gravel,bumpMap:gravel,bumpScale:.045,roughness:1}),
    wood:mat({map:wood,bumpMap:wood,bumpScale:.015,roughness:.64}),
    metal:mat({color:'#303634',metalness:.65,roughness:.36}),
    glass:new THREE.MeshPhysicalMaterial({color:'#94adb5',metalness:.12,roughness:.12,transparent:true,opacity:.25,envMapIntensity:.85,clearcoat:1,clearcoatRoughness:.1,side:THREE.DoubleSide,depthWrite:false}),
    fabric:mat({color:'#c6b9a4',roughness:1}),
    darkFabric:mat({color:'#888473',roughness:1}),
    soil:mat({color:'#665f49',roughness:1}),
    bark:mat({color:'#6d6551',roughness:1}),
    guide:new THREE.LineDashedMaterial({color:'#7b7b70',transparent:true,opacity:.36,dashSize:.16,gapSize:.12}),
  };
}
export function landscapeGrain() {
  return canvas(256,(ctx,n)=>{
    const rng=random(43),data=ctx.createImageData(n,n);
    for(let i=0;i<data.data.length;i+=4){const k=(rng()-.5)*24;data.data[i]=116+k;data.data[i+1]=132+k;data.data[i+2]=94+k;data.data[i+3]=255;}
    ctx.putImageData(data,0,0);
  });
}
export function environment(renderer) {
  const el=document.createElement('canvas');el.width=512;el.height=256;
  const ctx=el.getContext('2d'),g=ctx.createLinearGradient(0,0,0,256);
  g.addColorStop(0,'#b9d0df');g.addColorStop(.48,'#eef0e9');g.addColorStop(.55,'#e1d8c6');g.addColorStop(1,'#9b917c');ctx.fillStyle=g;ctx.fillRect(0,0,512,256);
  const glow=ctx.createRadialGradient(130,65,1,130,65,60);glow.addColorStop(0,'rgba(255,248,221,1)');glow.addColorStop(1,'rgba(255,248,221,0)');ctx.fillStyle=glow;ctx.fillRect(0,0,512,160);
  const tex=new THREE.CanvasTexture(el);tex.mapping=THREE.EquirectangularReflectionMapping;tex.colorSpace=THREE.SRGBColorSpace;
  const pmrem=new THREE.PMREMGenerator(renderer),target=pmrem.fromEquirectangular(tex);tex.dispose();pmrem.dispose();return target;
}
export function leafMaterial() {
  const texture=canvas(128,(ctx,n)=>{const rng=random(44);for(let i=0;i<200;i++){const x=rng()*n,y=rng()*n;const d=Math.hypot(x-n/2,y-n/2);if(d>n*.47)continue;const shade=60+Math.floor(rng()*70);ctx.fillStyle=`rgba(${shade},${shade+20},${shade-20},.86)`;ctx.beginPath();ctx.ellipse(x,y,2+rng()*5,1+rng()*3,rng()*Math.PI,0,Math.PI*2);ctx.fill();}});
  return new THREE.MeshStandardMaterial({map:texture,transparent:true,alphaTest:.4,side:THREE.DoubleSide,roughness:1,depthWrite:true});
}
