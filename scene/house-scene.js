import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { environment } from './materials.js';
const smooth=value=>{const n=THREE.MathUtils.clamp(value,0,1);return n*n*(3-2*n);};
// Blender study from a public render and unscaled plan; not an executive project.
export async function createHouseScene(container,{lowPower=false,onUnavailable=()=>{}}={}) {
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:lowPower?'low-power':'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,lowPower?1:1.4));
  renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.9;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;renderer.localClippingEnabled=true;
  const canvas=renderer.domElement;canvas.setAttribute('aria-hidden','true');canvas.dataset.engine='Blender GLB / Three.js';canvas.dataset.quality=lowPower?'compact':'full';
  const scene=new THREE.Scene(),env=environment(renderer);scene.environment=env.texture;scene.environmentIntensity=.4;
  scene.fog=new THREE.Fog('#111112',25,56);
  scene.add(new THREE.HemisphereLight('#e9ebf1','#19191b',.7));
  const sun=new THREE.DirectionalLight('#fff8ee',3.1);sun.position.set(-8,15,-9);sun.castShadow=true;
  sun.shadow.mapSize.set(lowPower?1024:2048,lowPower?1024:2048);Object.assign(sun.shadow.camera,{left:-12,right:12,top:12,bottom:-12,near:1,far:55});sun.shadow.normalBias=.025;sun.shadow.bias=-.00015;scene.add(sun);
  const edge=new THREE.DirectionalLight('#eef0f7',1.3);edge.position.set(10,8,5);scene.add(edge);
  const fill=new THREE.DirectionalLight('#f4f4f4',.45);fill.position.set(8,5,-8);scene.add(fill);
  const camera=new THREE.PerspectiveCamera(32,1,.1,100);
  let gltf;const draco=new DRACOLoader().setDecoderPath(new URL('./draco/',import.meta.url).href).setWorkerLimit(1);
  try{gltf=await new GLTFLoader().setDRACOLoader(draco).loadAsync(new URL('./models/residencia-rincao-v07.glb',import.meta.url).href);}catch(error){env.dispose();renderer.dispose();throw error;}finally{draco.dispose();}
  const model=gltf.scene;scene.add(model);model.updateMatrixWorld(true);
  const parts=[],materials=new Set(),geometries=new Set(),textures=new Set(),houseBounds=new THREE.Box3();
  model.traverse(mesh=>{
    if(!mesh.isMesh)return;
    const stage=Number(mesh.userData.buildStage??0),bounds=new THREE.Box3().setFromObject(mesh);
    mesh.castShadow=true;mesh.receiveShadow=true;geometries.add(mesh.geometry);
    const clipping=new THREE.Plane(new THREE.Vector3(0,-1,0),20);
    mesh.material=mesh.material.clone();materials.add(mesh.material);mesh.material.clippingPlanes=[clipping];mesh.material.clipShadows=true;
    Object.values(mesh.material).forEach(value=>{if(value?.isTexture)textures.add(value);});
    if(stage>0&&stage<6)houseBounds.union(bounds);
    if(mesh.material.name.includes('Vidro')){mesh.material.envMapIntensity=.85;mesh.material.transmission=0;mesh.material.transparent=true;mesh.material.opacity=.42;mesh.material.depthWrite=false;mesh.material.emissive.set('#a59981');mesh.material.emissiveIntensity=.08;}
    parts.push({mesh,stage,clipping,min:bounds.min.y,max:bounds.max.y});
  });
  const stageBounds=parts.reduce((all,p)=>{
    const bounds=all[p.stage]??={min:Infinity,max:-Infinity};
    bounds.min=Math.min(bounds.min,p.min);bounds.max=Math.max(bounds.max,p.max);return all;
  },{});
  const wire=new THREE.Group();scene.add(wire);
  parts.filter(p=>p.stage===2||p.stage===3).forEach(p=>{const geometry=new THREE.EdgesGeometry(p.mesh.geometry,35),material=new THREE.LineBasicMaterial({color:'#eeeeef',transparent:true,opacity:.4});const line=new THREE.LineSegments(geometry,material);line.applyMatrix4(p.mesh.matrixWorld);wire.add(line);});
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(100,100),new THREE.ShadowMaterial({opacity:.13}));floor.rotation.x=-Math.PI/2;floor.position.y=-.205;floor.receiveShadow=true;scene.add(floor);
  const outline=new THREE.Line(new THREE.BufferGeometry().setFromPoints([[3.25,-5.05],[-.05,-5.05],[-.05,-3.65],[-3.15,-3.65],[-3.15,5.05],[3.25,5.05],[3.25,-5.05]].map(([x,z])=>new THREE.Vector3(x,.01,z))),new THREE.LineDashedMaterial({color:'#a0a0a5',dashSize:.15,gapSize:.08,transparent:true,opacity:.65}));outline.computeLineDistances();scene.add(outline);
  let current=0,target=0,visible=true,disposed=false,raf=0,previous=0,w=1,h=1,pointerX=0,pointerY=0,px=0,py=0;
  // World-space reveals preserve dimensions: no squashed windows or floating pieces.
  const starts=[0,.04,.18,.34,.50,.67,.83],ends=[0,.17,.33,.49,.66,.82,.98];
  function pose(){
    for(const p of parts){const amount=p.stage===0?1:smooth((current-starts[p.stage])/(ends[p.stage]-starts[p.stage]));const bounds=stageBounds[p.stage];p.mesh.visible=amount>.001;p.clipping.constant=bounds.min-.015+(bounds.max-bounds.min+.03)*amount;}
    outline.visible=current<.35;outline.material.opacity=.65*(1-smooth(current/.35));
    wire.visible=current<.22;wire.children.forEach(line=>line.material.opacity=.45*(1-smooth(current/.22)));
    const aspect=w/h;
    // Portrait/tablet frames need horizontal breathing room, not desktop cropping.
    const size=houseBounds.getSize(new THREE.Vector3()),azimuth=.46+px*.012;
    const width=Math.cos(azimuth)*size.x+Math.sin(azimuth)*size.z;
    const depth=Math.sin(azimuth)*size.x+Math.cos(azimuth)*size.z;
    const halfFov=Math.tan(THREE.MathUtils.degToRad(camera.fov/2));
    const distance=Math.max(width/(2*halfFov*aspect),(size.y+depth*.12)/(2*halfFov))*1.14+depth*.2;
    scene.fog.near=distance+7;scene.fog.far=distance+45;
    // Eye-level façade; fixed viewpoint throughout every construction stage.
    camera.position.set(-Math.sin(azimuth)*distance,3.8+py*.07,-Math.cos(azimuth)*distance);camera.lookAt(-.7,1.8,-.25);
    sun.color.setRGB(1,.98-.035*current,.97-.075*current);
  }
  function draw(time=performance.now()){
    raf=0;if(!visible||disposed||document.hidden)return;
    const delta=Math.min(.05,(time-previous)/1000||.016);previous=time;const a=1-Math.exp(-9*delta);
    current+=(target-current)*a;
    px+=(pointerX-px)*a;py+=(pointerY-py)*a;
    if(Math.abs(target-current)<.0003)current=target;
    pose();const start=performance.now();renderer.render(scene,camera);
    canvas.dataset.progress=current.toFixed(3);canvas.dataset.drawCalls=String(renderer.info.render.calls);canvas.dataset.triangles=String(renderer.info.render.triangles);canvas.dataset.renderMs=(performance.now()-start).toFixed(1);
    if(Math.abs(target-current)>.0003||Math.abs(px-pointerX)+Math.abs(py-pointerY)>.001)raf=requestAnimationFrame(draw);else canvas.dataset.rendering='idle';
  }
  function schedule(){if(!raf&&visible&&!disposed&&!document.hidden){canvas.dataset.rendering='active';previous=performance.now();raf=requestAnimationFrame(draw);}}
  function resize(){w=Math.max(1,container.clientWidth);h=Math.max(1,container.clientHeight);camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);schedule();}
  const ro=new ResizeObserver(resize);ro.observe(container);
  const hidden=()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;}else schedule();};document.addEventListener('visibilitychange',hidden);
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();onUnavailable();dispose();});
  function dispose(){if(disposed)return;disposed=true;cancelAnimationFrame(raf);ro.disconnect();document.removeEventListener('visibilitychange',hidden);geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());wire.children.forEach(line=>{line.geometry.dispose();line.material.dispose();});floor.geometry.dispose();floor.material.dispose();outline.geometry.dispose();outline.material.dispose();env.dispose();renderer.dispose();canvas.remove();}
  container.append(canvas);resize();await renderer.compileAsync(scene,camera);pose();renderer.render(scene,camera);
  return {
    setProgress(value,immediate=false){target=THREE.MathUtils.clamp(value,0,1);if(immediate)current=target;schedule();},
    setPointer(x,y){pointerX=THREE.MathUtils.clamp(x,-1,1);pointerY=THREE.MathUtils.clamp(y,-1,1);schedule();},
    setVisible(value){visible=value;if(!value){cancelAnimationFrame(raf);raf=0;canvas.dataset.rendering='paused';}else schedule();},
    async capture(){current=1;pose();renderer.render(scene,camera);return new Promise(resolve=>canvas.toBlob(resolve,'image/webp',.94));},
    dispose,
  };
}
