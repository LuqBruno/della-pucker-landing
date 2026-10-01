import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { createMaterials, environment, leafMaterial, random } from './materials.js';

const clamp = THREE.MathUtils.clamp;
const smooth = value => { const n=clamp(value,0,1); return n*n*(3-2*n); };

// Original conceptual residence, not a project attributed to Della & Pucker.
// Model units: metres. RC frame, masonry infill, flat roof with parapet.
export async function createHouseScene(container, {lowPower=false, onUnavailable=()=>{}}={}) {
  const renderer = new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:lowPower?'low-power':'high-performance'});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, lowPower?1.25:1.75));
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure=.92;
  renderer.shadowMap.enabled=true;
  renderer.shadowMap.type=THREE.PCFShadowMap;
  renderer.domElement.setAttribute('aria-hidden','true');
  renderer.domElement.dataset.quality=lowPower?'compact':'full';
  const scene=new THREE.Scene();scene.background=new THREE.Color('#e5e1d7');
  scene.fog=new THREE.Fog('#e5e1d7',65,110);
  const camera=new THREE.PerspectiveCamera(33,1,.1,150);
  const env=environment(renderer);scene.environment=env.texture;scene.environmentIntensity=.75;
  scene.add(new THREE.HemisphereLight('#edf4fa','#b5aa91',.9));
  const sun=new THREE.DirectionalLight('#fff1d3',2.8);sun.position.set(-10,17,8);sun.castShadow=true;
  sun.shadow.mapSize.set(lowPower?1024:2048,lowPower?1024:2048);
  Object.assign(sun.shadow.camera,{left:-17,right:17,top:17,bottom:-17,near:1,far:65});
  sun.shadow.bias=-.00015;sun.shadow.normalBias=.035;sun.shadow.radius=3;scene.add(sun);
  const fill=new THREE.DirectionalLight('#c0d8e7',.55);fill.position.set(10,8,-8);scene.add(fill);
  const model=new THREE.Group();scene.add(model);
  const materials=createMaterials(lowPower),parts=[],geometries=new Set(),extraMaterials=new Set();
  const unitBox=new THREE.BoxGeometry(1,1,1);geometries.add(unitBox);
  function part(object,start,end,mode='rise',bottom=0) {
    if(mode==='fade'){object.material=object.material.clone();object.material.transparent=false;object.material.alphaHash=true;extraMaterials.add(object.material);}
    const basePosition=object.position.clone(),baseScale=object.scale.clone();
    model.add(object);parts.push({object,start,end,mode,bottom,basePosition,baseScale});return object;
  }
  function box(w,h,d,x,y,z,material,start=0,end=0,mode='rise',bevel=0) {
    const geo=bevel?new RoundedBoxGeometry(w,h,d,1,bevel):unitBox;
    if(bevel)geometries.add(geo);
    const mesh=new THREE.Mesh(geo,material);if(!bevel)mesh.scale.set(w,h,d);
    mesh.position.set(x,y+h/2,z);mesh.castShadow=true;mesh.receiveShadow=true;
    if(end>start)part(mesh,start,end,mode,y);else model.add(mesh);return mesh;
  }
  // The footprint stays in place. Elements grow from their support rather than flying in.
  box(20,.16,16,0,-.18,0,materials.ground);
  const backdrop=new THREE.Mesh(new THREE.PlaneGeometry(180,180),new THREE.MeshStandardMaterial({color:'#e5e1d7',roughness:1}));backdrop.rotation.x=-Math.PI/2;backdrop.position.y=-.19;backdrop.receiveShadow=true;scene.add(backdrop);geometries.add(backdrop.geometry);extraMaterials.add(backdrop.material);
  const contactCanvas=document.createElement('canvas');contactCanvas.width=contactCanvas.height=512;
  const contactContext=contactCanvas.getContext('2d');contactContext.shadowColor='rgba(0,0,0,.65)';contactContext.shadowBlur=18;contactContext.fillStyle='rgba(0,0,0,.55)';
  contactContext.beginPath();contactContext.moveTo(99,139);contactContext.lineTo(417,139);contactContext.lineTo(417,394);contactContext.lineTo(323,394);contactContext.lineTo(323,360);contactContext.lineTo(99,360);contactContext.closePath();contactContext.fill();
  const contactTexture=new THREE.CanvasTexture(contactCanvas),contactMaterial=new THREE.MeshBasicMaterial({map:contactTexture,transparent:true,opacity:.4,depthWrite:false});
  const contact=new THREE.Mesh(new THREE.PlaneGeometry(20,16),contactMaterial);contact.rotation.x=-Math.PI/2;contact.position.y=.008;model.add(contact);geometries.add(contact.geometry);extraMaterials.add(contactMaterial);
  const linePoints=[[-6.15,0,-3.7],[6.35,0,-3.7],[6.35,0,4.3],[2.6,0,4.3],[2.6,0,3.2],[-6.15,0,3.2],[-6.15,0,-3.7]];
  const plotGuide=new THREE.Line(new THREE.BufferGeometry().setFromPoints(linePoints.map(p=>new THREE.Vector3(...p))),materials.guide);plotGuide.computeLineDistances();plotGuide.position.y=.015;model.add(plotGuide);geometries.add(plotGuide.geometry);
  const future=new THREE.Group(),ghostMat=materials.guide.clone();ghostMat.opacity=.2;extraMaterials.add(ghostMat);
  const ghostLines=[...linePoints.map(([x,,z])=>new THREE.Vector3(x,3.55,z)),new THREE.Vector3(-6.15,3.55,-3.7)];
  const roofGuide=new THREE.Line(new THREE.BufferGeometry().setFromPoints(ghostLines),ghostMat);roofGuide.computeLineDistances();future.add(roofGuide);geometries.add(roofGuide.geometry);
  for(const [x,,z] of linePoints.slice(0,-1)){const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x,.03,z),new THREE.Vector3(x,3.55,z)]),ghostMat);line.computeLineDistances();future.add(line);geometries.add(line.geometry);}model.add(future);
  // 01 + 02: compacted base, footing pads and grade beams.
  box(12.55,.08,8.1,.1,-.02,.25,materials.stone,.01,.1);
  const columns=[[-5.85,-3.35],[-1.6,-3.35],[2.65,-3.35],[6.05,-3.35],[-5.85,2.9],[-1.6,2.9],[2.65,2.9],[6.05,3.9]];
  columns.forEach(([x,z],i)=>box(1.1,.36,1.1,x,-.03,z,materials.concrete,.09+i*.003,.18+i*.003));
  box(12.05,.34,.32,.1,.02,-3.35,materials.concrete,.12,.23);
  box(8.5,.34,.32,-1.6,.02,2.9,materials.concrete,.12,.23);
  box(3.4,.34,.32,4.35,.02,3.9,materials.concrete,.14,.24);
  [-5.85,2.65,6.05].forEach((x,i)=>box(.32,.34,x===6.05?7.25:6.25,x,.02,x===6.05?.275:-.225,materials.concrete,.12+i*.01,.24+i*.01));
  box(8.8,.18,6.7,-1.6,.32,-.2,materials.concrete,.2,.28);
  box(3.65,.18,7.75,4.35,.32,.3,materials.concrete,.2,.28);
  // 03: reinforced concrete columns and connected beams.
  columns.forEach(([x,z],i)=>box(.24,x>5?3.1:2.85,.24,x,.5,z,materials.concrete,.25+i*.009,.37+i*.009));
  box(8.75,.26,.28,-1.6,3.22,-3.35,materials.concrete,.37,.45,'wipe');
  box(8.75,.26,.28,-1.6,3.22,2.9,materials.concrete,.38,.46,'wipe');
  [-5.85,2.65].forEach(x=>box(.28,.26,6.5,x,3.22,-.225,materials.concrete,.38,.46,'wipe'));
  box(3.65,.26,.28,4.35,3.48,3.9,materials.concrete,.39,.47,'wipe');
  box(3.65,.26,.28,4.35,3.48,-3.35,materials.concrete,.39,.47,'wipe');
  box(.28,.26,7.5,6.05,3.48,.275,materials.concrete,.4,.48,'wipe');
  // 04: masonry has real openings, not a glass plane pasted onto a solid wall.
  const walls=[];
  const wall=(w,h,d,x,y,z,start=.44)=>{box(w,h,d,x,y,z,materials.masonry,start,start+.14);walls.push({w,h,d,x,y,z});};
  wall(12.05,2.75,.22,.1,.5,-3.35);
  wall(.22,2.75,6.25,-5.85,.5,-.225,.46);
  wall(.22,1.3,7.25,6.05,.5,.275,.46);
  wall(.22,.86,7.25,6.05,2.64,.275,.46);
  wall(.22,.84,4.65,6.05,1.8,-1.025,.46);
  wall(.22,.84,.8,6.05,1.8,3.5,.46);
  wall(.22,2.75,5.35,2.65,.5,-.65,.47);
  // Right-wing front window sill, lintel and jambs.
  wall(3.4,1.05,.22,4.35,.5,3.9,.48);wall(3.4,.86,.22,4.35,2.69,3.9,.48);
  wall(.45,1.14,.22,2.875,1.55,3.9,.48);wall(.45,1.14,.22,5.825,1.55,3.9,.48);
  // Main entrance: a 1.0 m door and a side panel alongside the glazed living room.
  wall(.72,2.75,.22,-5.49,.5,2.9,.48);wall(.2,2.75,.22,-3.86,.5,2.9,.49);
  wall(1.07,.28,.22,-4.59,2.97,2.9,.49);
  // Roof deck, overhang and waterproofing gravel inside shallow parapets.
  box(9.5,.22,7.55,-1.6,3.48,-.1,materials.concrete,.57,.65);
  box(3.95,.22,8.05,4.35,3.73,.275,materials.concrete,.58,.66);
  box(8.99,.06,6.99,-1.6,3.71,-.1,materials.gravel,.63,.7);
  box(3.45,.06,7.54,4.35,3.96,.275,materials.gravel,.63,.7);
  for(const z of [-3.8,3.6])box(9.5,.22,.14,-1.6,3.7,z,materials.concrete,.62,.7,'wipe');
  for(const x of [-6.28,3.08])box(.14,.22,7.4,x,3.7,-.1,materials.concrete,.62,.7,'wipe');
  for(const z of [-3.68,4.23])box(3.95,.25,.14,4.35,3.95,z,materials.plaster,.64,.72,'wipe');
  for(const x of [2.45,6.25])box(.14,.25,7.9,x,3.95,.275,materials.plaster,.64,.72,'wipe');
  // 05: plaster, aluminium frames, glazing and wooden joinery.
  walls.forEach(({w,h,d,x,y,z},i)=>box(w+.012,h+.005,d+.012,x,y,z,materials.plaster,.7+i*.001,.8+i*.001));
  const glazing=(x,z,w,h,bottom,side=false)=>{
    const d=.045,frame=.065;
    box(side?d:w,h,side?w:d,x,bottom,z,materials.glass,.69,.8);
    for(const yy of [bottom,bottom+h-frame])box(side?.09:w,frame,side?w:.09,x,yy,z,materials.metal,.7,.81);
    const count=Math.max(1,Math.round(w/1.45));
    for(let i=0;i<=count;i++){const k=-w/2+i*w/count;box(side?.09:frame,h,side?frame:.09,x+(side?0:k),bottom,z+(side?k:0),materials.metal,.71+i*.003,.82+i*.003);}
  };
  glazing(-.54,2.99,6.5,2.67,.5);glazing(4.35,4.01,2.5,1.08,1.57);glazing(6.17,2.2,1.8,.8,1.82,true);
  box(9.5,.23,.035,-1.6,3.48,3.69,materials.metal,.76,.86,'wipe');
  box(.035,.23,7.55,-6.365,3.48,-.1,materials.metal,.76,.86,'wipe');
  box(1.0,2.46,.065,-4.6,.5,3.02,materials.wood,.72,.82);
  box(.035,.38,.075,-4.19,1.36,3.07,materials.metal,.78,.85);
  // Slatted entry screen is instanced to keep draw calls under control.
  const slats=new THREE.InstancedMesh(new THREE.BoxGeometry(.044,2.75,.09),materials.wood,17);geometries.add(slats.geometry);const transform=new THREE.Object3D();
  for(let i=0;i<17;i++){transform.position.set(-5.825+i*.045,.5+2.75/2,3.055);transform.updateMatrix();slats.setMatrixAt(i,transform.matrix);}slats.castShadow=true;slats.receiveShadow=true;part(slats,.75,.84,'fade');
  box(8.6,.012,6.2,-1.6,.502,-.2,materials.stone,.77,.86);
  // Furnished living room and rear kitchen: visible through glazing, no empty shell.
  box(2.9,.38,.86,-.15,.52,.05,materials.fabric,.79,.88,'rise',.07);
  box(2.9,.62,.22,-.15,.67,-.34,materials.fabric,.79,.88,'rise',.045);
  [-1.49,1.19].forEach(x=>box(.22,.6,.95,x,.54,.06,materials.fabric,.8,.89,'rise',.045));
  [-.95,-.13,.68].forEach(x=>box(.75,.11,.71,x,.89,.1,materials.darkFabric,.81,.9,'rise',.03));
  box(1.45,.065,.72,-.2,.79,1.48,materials.wood,.8,.9,'rise',.015);
  [-.8,.4].forEach(x=>box(.035,.26,.58,x,.53,1.48,materials.metal,.8,.9));
  box(3.1,.012,2.4,-.2,.514,.95,materials.darkFabric,.79,.88);
  box(3.9,.9,.65,-2.6,.52,-2.85,materials.wood,.8,.89);box(4,.055,.71,-2.6,1.42,-2.85,materials.stone,.8,.89);
  box(1.1,2.55,.6,-5,.52,-2.8,materials.metal,.81,.9);
  // 06: exterior paving, rain line, restrained landscaping and human-scale steps.
  box(10.0,.12,1.35,-1.35,.17,3.7,materials.stone,.85,.93);
  box(3.1,.095,.55,-4.45,.075,4.63,materials.concrete,.86,.94);
  box(3.1,.075,.55,-4.45,.002,5.14,materials.concrete,.87,.95);
  for(let i=0;i<4;i++)box(2.1,.07,.53,-4.45,.01,5.83+i*.72,materials.stone,.87+i*.005,.96);
  box(3.1,.03,7.8,8.1,-.006,.15,materials.lawn,.86,.94);
  box(13,.03,2.0,.2,-.006,6.68,materials.lawn,.86,.94);
  box(2.1,.03,7.8,-8,-.006,.15,materials.lawn,.86,.94);
  box(.07,3.0,.07,6.2,.23,-3.4,materials.metal,.86,.95);
  // Thin timber battens beneath the concrete canopy add scale without ornament.
  for(let i=0;i<12;i++)box(.07,.055,6.6,-5.8+i*.72,3.46,-.1,materials.wood,.79,.88,'fade');
  const leaves=leafMaterial();extraMaterials.add(leaves);const rng=random(33);
  const leafGeo=new THREE.PlaneGeometry(1,1);geometries.add(leafGeo);
  const plantCount=lowPower?42:90,plants=new THREE.InstancedMesh(leafGeo,leaves,plantCount);
  for(let i=0;i<plantCount;i++){const x=i<plantCount*.7?7.1+rng()*1.1:-7.7+rng()*.9,z=-3.2+rng()*7.0;transform.position.set(x,.23+rng()*.28,z);transform.rotation.set(-.2+rng()*.4,rng()*Math.PI,0);transform.scale.set(.55+rng()*.45,.5+rng()*.55,1);transform.updateMatrix();plants.setMatrixAt(i,transform.matrix);}plants.castShadow=true;part(plants,.88,.98,'fade');
  // One light, irregular tree at the rear: textured leaf clusters, not solid spheres.
  const trunk=new THREE.Mesh(new THREE.CylinderGeometry(.055,.11,3.4,8),materials.bark);trunk.position.set(7.55,1.7,-4.85);geometries.add(trunk.geometry);trunk.castShadow=true;part(trunk,.88,.97,'fade');
  for(let i=0;i<5;i++){const angle=i*Math.PI*.4;const start=new THREE.Vector3(7.55,2.25+i*.12,-4.85),end=new THREE.Vector3(7.55+Math.sin(angle)*.75,3.5+i*.1,-4.85+Math.cos(angle)*.75);const direction=end.clone().sub(start);const branch=new THREE.Mesh(new THREE.CylinderGeometry(.018,.032,direction.length(),6),materials.bark);branch.position.copy(start.clone().add(end).multiplyScalar(.5));branch.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),direction.normalize());branch.castShadow=true;geometries.add(branch.geometry);part(branch,.89,.98,'fade');}
  const canopyCount=lowPower?18:34,canopy=new THREE.InstancedMesh(leafGeo,leaves,canopyCount);
  for(let i=0;i<canopyCount;i++){transform.position.set(7.55+(rng()-.5)*2.3,3.05+rng()*1.35,-4.85+(rng()-.5)*2.1);transform.rotation.set((rng()-.5)*1.1,rng()*Math.PI,0);transform.scale.set(1.1+rng()*.8,1.05+rng()*.9,1);transform.updateMatrix();canopy.setMatrixAt(i,transform.matrix);}canopy.castShadow=true;part(canopy,.89,.98,'fade');

  let current=0,target=0,visible=true,disposed=false,raf=0,previous=0,pointerX=0,pointerY=0,viewX=0,viewY=0;
  let w=1,h=1,lastMs=0;
  function pose(progress) {
    for(const p of parts){const amount=smooth((progress-p.start)/(p.end-p.start));p.object.visible=amount>.001;
      if(!p.object.visible)continue;
      p.object.position.copy(p.basePosition);p.object.scale.copy(p.baseScale);
      if(p.mode==='rise') {p.object.scale.y=p.baseScale.y*Math.max(.001,amount);p.object.position.y=p.bottom+(p.basePosition.y-p.bottom)*amount;}
      if(p.mode==='wipe'){p.object.scale.x=p.baseScale.x*Math.max(.001,amount);p.object.position.x=p.basePosition.x-(1-amount)*(p.object.geometry===unitBox?p.baseScale.x:0)/2;}
      // Fade meshes are already physically attached. Dithering avoids sorting artefacts.
      if(p.mode==='fade') p.object.material.opacity=amount;
    }
    ghostMat.opacity=.24*(1-smooth((progress-.18)/.4));future.visible=progress<.62;
    contactMaterial.opacity=.45*smooth((progress-.09)/.18);
    const t=smooth(progress),distance=31.7*Math.max(1,1.22/(w/h));
    const angle=.72+t*.095+viewX*.035,elevation=.47-t*.12+viewY*.022;
    camera.position.set(Math.sin(angle)*Math.cos(elevation)*distance,1.3+Math.sin(elevation)*distance,Math.cos(angle)*Math.cos(elevation)*distance);
    camera.lookAt(0,1.35,.45);
  }
  function draw(time=performance.now()) {
    raf=0;if(!visible||disposed||document.hidden)return;
    const delta=Math.min(.06,(time-previous)/1000||.016);previous=time;
    const a=1-Math.exp(-10*delta);current+= (target-current)*a;viewX+=(pointerX-viewX)*a;viewY+=(pointerY-viewY)*a;
    if(Math.abs(target-current)<.0005)current=target;
    const start=performance.now();pose(current);renderer.render(scene,camera);lastMs=performance.now()-start;
    const el=renderer.domElement;el.dataset.progress=current.toFixed(3);el.dataset.drawCalls=String(renderer.info.render.calls);el.dataset.triangles=String(renderer.info.render.triangles);el.dataset.renderMs=lastMs.toFixed(1);
    if(Math.abs(target-current)>.0005||Math.abs(pointerX-viewX)>.002||Math.abs(pointerY-viewY)>.002)raf=requestAnimationFrame(draw);else el.dataset.rendering='idle';
  }
  function schedule(){if(!raf&&visible&&!disposed&&!document.hidden){renderer.domElement.dataset.rendering='active';previous=performance.now();raf=requestAnimationFrame(draw);}}
  function resize(){w=Math.max(1,container.clientWidth);h=Math.max(1,container.clientHeight);camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);schedule();}
  const ro=new ResizeObserver(resize);ro.observe(container);
  const handleMove=event=>{if(lowPower||!matchMedia('(pointer:fine)').matches)return;const r=container.getBoundingClientRect();pointerX=(event.clientX-r.left)/r.width-.5;pointerY=(event.clientY-r.top)/r.height-.5;schedule();};
  const handleLeave=()=>{pointerX=pointerY=0;schedule();};
  container.addEventListener('pointermove',handleMove,{passive:true});container.addEventListener('pointerleave',handleLeave);
  const handleHidden=()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;}else schedule();};document.addEventListener('visibilitychange',handleHidden);
  renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();onUnavailable();dispose();});
  resize();await renderer.compileAsync(scene,camera);container.append(renderer.domElement);pose(0);renderer.render(scene,camera);
  function dispose(){if(disposed)return;disposed=true;cancelAnimationFrame(raf);ro.disconnect();container.removeEventListener('pointermove',handleMove);container.removeEventListener('pointerleave',handleLeave);document.removeEventListener('visibilitychange',handleHidden);geometries.forEach(g=>g.dispose());const allMats=new Set([...Object.values(materials),...extraMaterials]);allMats.forEach(m=>{['map','bumpMap'].forEach(key=>m[key]?.dispose());m.dispose();});env.dispose();renderer.dispose();renderer.domElement.remove();}
  return {
    setProgress(value,immediate=false){target=clamp(value,0,1);if(immediate)current=target;schedule();},
    setVisible(value){visible=value;if(!value){cancelAnimationFrame(raf);raf=0;renderer.domElement.dataset.rendering='paused';}else schedule();},
    async capture(){pose(1);renderer.render(scene,camera);return await new Promise(resolve=>renderer.domElement.toBlob(resolve,'image/webp',.9));},
    dispose,
  };
}
