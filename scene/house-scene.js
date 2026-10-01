import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { environment } from './materials.js';
const smooth=value=>{const n=THREE.MathUtils.clamp(value,0,1);return n*n*(3-2*n);};
// Blender camera of render_v08.py (Z-up) converted to glTF/three (Y-up): (x,y,z) -> (x,z,-y).
const BLENDER_CAMERA={position:new THREE.Vector3(-12.6,3.7,-25.8),target:new THREE.Vector3(-.7,1.55,-1.0),lens:46,sensor:36};
const cold=new THREE.Color('#dfe6f2'),warm=new THREE.Color('#fff1dc'),amber=new THREE.Color('#d9a35e');
// Blender study from a public render and unscaled plan; not an executive project.
export async function createHouseScene(container,{lowPower=false,frame,onUnavailable=()=>{}}={}) {
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:lowPower?'low-power':'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,lowPower?1:1.25));
  renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.AgXToneMapping;renderer.toneMappingExposure=1.05;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;renderer.localClippingEnabled=true;
  const canvas=renderer.domElement;canvas.setAttribute('aria-hidden','true');canvas.dataset.engine='Blender GLB / Three.js';canvas.dataset.quality=lowPower?'compact':'full';
  const scene=new THREE.Scene(),env=environment(renderer);scene.environment=env.texture;scene.environmentIntensity=.42;
  scene.add(new THREE.HemisphereLight('#e9ebf1','#19191b',.6));
  const sun=new THREE.DirectionalLight('#fff8ee',3.1);sun.position.set(-7,10,-13);sun.castShadow=true;
  sun.shadow.mapSize.set(lowPower?1024:2048,lowPower?1024:2048);Object.assign(sun.shadow.camera,{left:-12,right:12,top:12,bottom:-12,near:1,far:55});sun.shadow.normalBias=.025;sun.shadow.bias=-.00015;scene.add(sun);
  const rim=new THREE.DirectionalLight('#eef0f7',1.4);rim.position.set(6,12,5);scene.add(rim);
  const fill=new THREE.DirectionalLight('#f4f4f4',.4);fill.position.set(-10,6,2);scene.add(fill);
  const interior=new THREE.PointLight('#ffb36b',0,9,1.6);interior.position.set(1.1,1.4,-2.7);scene.add(interior);
  // Same frame as the Blender render: the poster is a crop of it, so geometry lines up on swap.
  const renderAspect=frame?frame.w/frame.h:1.6;
  const camera=new THREE.PerspectiveCamera(THREE.MathUtils.radToDeg(2*Math.atan(BLENDER_CAMERA.sensor/2/BLENDER_CAMERA.lens/renderAspect)),renderAspect,.1,120);
  let gltf;const draco=new DRACOLoader().setDecoderPath(new URL('./draco/',import.meta.url).href).setWorkerLimit(1);
  try{gltf=await new GLTFLoader().setDRACOLoader(draco).loadAsync(new URL('./models/residencia-rincao-v07.glb',import.meta.url).href);}catch(error){env.dispose();renderer.dispose();throw error;}finally{draco.dispose();}
  const model=gltf.scene;scene.add(model);model.updateMatrixWorld(true);
  let floorY=-.205;const parts=[],materials=new Set(),geometries=new Set(),textures=new Set(),glass=[];
  model.traverse(mesh=>{
    if(!mesh.isMesh)return;
    const stage=Number(mesh.userData.buildStage??0),bounds=new THREE.Box3().setFromObject(mesh);geometries.add(mesh.geometry);
    // The editorial ground becomes a shadow-only plane, like the shadow catcher of the poster.
    if(mesh.material.name.startsWith('Solo editorial')){floorY=bounds.max.y;mesh.visible=false;materials.add(mesh.material);return;}
    mesh.castShadow=true;mesh.receiveShadow=true;geometries.add(mesh.geometry);
    const clipping=new THREE.Plane(new THREE.Vector3(0,-1,0),20);
    mesh.material=mesh.material.clone();materials.add(mesh.material);mesh.material.clippingPlanes=[clipping];mesh.material.clipShadows=true;
    Object.values(mesh.material).forEach(value=>{if(value?.isTexture)textures.add(value);});
    if(mesh.material.name.includes('Vidro')){Object.assign(mesh.material,{envMapIntensity:.9,transmission:0,transparent:true,opacity:.5,depthWrite:false});mesh.material.emissive.copy(amber);mesh.material.emissiveIntensity=0;glass.push(mesh.material);}
    parts.push({mesh,stage,clipping,min:bounds.min.y,max:bounds.max.y});
  });
  const stageBounds=parts.reduce((all,p)=>{
    const bounds=all[p.stage]??={min:Infinity,max:-Infinity};
    bounds.min=Math.min(bounds.min,p.min);bounds.max=Math.max(bounds.max,p.max);return all;
  },{});
  // "Linhas de projeto": thin white edges of the whole house, drawn before any solid exists.
  const wire=new THREE.Group(),wireMaterial=new THREE.LineBasicMaterial({color:'#f2efe8',transparent:true,opacity:.5,depthWrite:false});scene.add(wire);
  parts.filter(p=>p.stage>=1&&p.stage<=5).forEach(p=>{const geometry=new THREE.EdgesGeometry(p.mesh.geometry,32);const line=new THREE.LineSegments(geometry,wireMaterial);line.applyMatrix4(p.mesh.matrixWorld);wire.add(line);});
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(100,100),new THREE.ShadowMaterial({opacity:.32}));floor.rotation.x=-Math.PI/2;floor.position.y=floorY+.002;floor.receiveShadow=true;scene.add(floor);
  const outline=new THREE.Line(new THREE.BufferGeometry().setFromPoints([[3.25,-5.05],[-.05,-5.05],[-.05,-3.65],[-3.15,-3.65],[-3.15,5.05],[3.25,5.05],[3.25,-5.05]].map(([x,z])=>new THREE.Vector3(x,.01,z))),new THREE.LineDashedMaterial({color:'#bdbcb6',dashSize:.15,gapSize:.08,transparent:true,opacity:.7}));outline.computeLineDistances();scene.add(outline);
  let current=0,target=0,visible=true,disposed=false,raf=0,previous=0,pointerX=0,pointerY=0,px=0,py=0;
  // World-space reveals preserve dimensions: no squashed windows or floating pieces.
  const starts=[0,.06,.2,.35,.51,.67,.82],ends=[0,.19,.34,.5,.66,.81,.96];
  const offset=new THREE.Vector3(),tint=new THREE.Color();
  function pose(){
    for(const p of parts){const amount=p.stage===0?1:smooth((current-starts[p.stage])/(ends[p.stage]-starts[p.stage]));const bounds=stageBounds[p.stage];p.mesh.visible=amount>.001;p.clipping.constant=bounds.min-.015+(bounds.max-bounds.min+.03)*amount;}
    outline.visible=current<.4;outline.material.opacity=.7*(1-smooth(current/.4));
    wireMaterial.opacity=.55*(1-smooth((current-.18)/.5));wire.visible=wireMaterial.opacity>.005;
    // Light drifts from cool daylight to warm evening; windows glow only once glazed.
    sun.color.copy(tint.copy(cold).lerp(warm,smooth(current)));sun.intensity=2.6+.6*current;
    const glow=smooth((current-.8)/.18);glass.forEach(m=>m.emissiveIntensity=.55*glow);interior.intensity=14*glow;
    // Fixed viewpoint; pointer adds a few centimetres of parallax on desktop only.
    offset.set(px*.35,-py*.16,0);camera.position.copy(BLENDER_CAMERA.position).add(offset);camera.lookAt(BLENDER_CAMERA.target);
  }
  function draw(time=performance.now()){
    raf=0;if(!visible||disposed||document.hidden)return;
    const delta=Math.min(.05,(time-previous)/1000||.016);previous=time;const a=1-Math.exp(-9*delta);
    current+=(target-current)*a;px+=(pointerX-px)*a;py+=(pointerY-py)*a;
    if(Math.abs(target-current)<.0003)current=target;
    pose();const start=performance.now();renderer.render(scene,camera);
    canvas.dataset.progress=current.toFixed(3);canvas.dataset.drawCalls=String(renderer.info.render.calls);canvas.dataset.triangles=String(renderer.info.render.triangles);canvas.dataset.renderMs=(performance.now()-start).toFixed(1);
    if(Math.abs(target-current)>.0003||Math.abs(px-pointerX)+Math.abs(py-pointerY)>.001)raf=requestAnimationFrame(draw);else canvas.dataset.rendering='idle';
  }
  function schedule(){if(!raf&&visible&&!disposed&&!document.hidden){canvas.dataset.rendering='active';previous=performance.now();raf=requestAnimationFrame(draw);}}
  function resize(){
    // The container matches the cropped poster; the canvas covers the full render frame behind it.
    const cw=Math.max(1,container.clientWidth),scale=frame?cw/frame.cw:1,w=Math.round(frame?frame.w*scale:cw),h=Math.round(frame?frame.h*scale:container.clientHeight);
    Object.assign(canvas.style,{width:w+'px',height:h+'px',left:-(frame?frame.x0*scale:0)+'px',top:-(frame?frame.y0*scale:0)+'px'});
    renderer.setSize(w,h,false);schedule();
  }
  const ro=new ResizeObserver(resize);ro.observe(container);
  const hidden=()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;}else schedule();};document.addEventListener('visibilitychange',hidden);
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();onUnavailable();dispose();});
  function dispose(){if(disposed)return;disposed=true;cancelAnimationFrame(raf);ro.disconnect();document.removeEventListener('visibilitychange',hidden);geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());wire.children.forEach(line=>line.geometry.dispose());wireMaterial.dispose();floor.geometry.dispose();floor.material.dispose();outline.geometry.dispose();outline.material.dispose();env.dispose();renderer.dispose();canvas.remove();}
  container.append(canvas);resize();await renderer.compileAsync(scene,camera);current=target=1;pose();renderer.render(scene,camera);
  return {
    setProgress(value,immediate=false){target=THREE.MathUtils.clamp(value,0,1);if(immediate)current=target;schedule();},
    setPointer(x,y){pointerX=THREE.MathUtils.clamp(x,-1,1);pointerY=THREE.MathUtils.clamp(y,-1,1);schedule();},
    setVisible(value){visible=value;if(!value){cancelAnimationFrame(raf);raf=0;canvas.dataset.rendering='paused';}else schedule();},
    dispose,
  };
}
