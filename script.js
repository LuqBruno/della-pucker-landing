import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
import { initProjectGallery } from './gallery.js';
gsap.registerPlugin(ScrollTrigger);
ScrollTrigger.config({ignoreMobileResize:true});

const root=document.documentElement,story=document.querySelector('.hero'),hero=document.querySelector('#construction-story');
const art=document.querySelector('.hero-art'),host=document.querySelector('.house-canvas'),poster=document.querySelector('.house-poster'),topbar=document.querySelector('.topbar');
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),desktop=matchMedia('(min-width:1024px) and (hover:hover) and (pointer:fine)'),params=new URLSearchParams(location.search);
const connection=navigator.connection;
const limited=()=>connection?.saveData||/(^|-)(2g|3g)$/.test(connection?.effectiveType||'')||(navigator.hardwareConcurrency&&navigator.hardwareConcurrency<=2)||(navigator.deviceMemory&&navigator.deviceMemory<=2);
const motionOff=()=>reduced.matches||params.get('motion')==='reduce';
const webgl=(()=>{let ok;return()=>ok??=(()=>{try{return !!document.createElement('canvas').getContext('webgl2');}catch{return false;}})();})();
const staticOnly=()=>motionOff()||params.get('renderer')==='static'||!desktop.matches||limited()||!webgl();
root.classList.add('js');
const lifetime=new AbortController(),listen=(target,type,fn,options={})=>target?.addEventListener(type,fn,{...options,signal:lifetime.signal});

// Contact: same public number everywhere, one coherent message. Nothing is sent automatically.
const message='Olá, gostaria de conversar com a Della & Pucker sobre um projeto. Podem me orientar sobre o orçamento?';
document.querySelectorAll('[data-contact]').forEach(link=>link.href='https://wa.me/554834127737?text='+encodeURIComponent(message));

let gallery={destroy(){}};
const galleryObserver=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)return;galleryObserver.disconnect();gallery=initProjectGallery();},{rootMargin:'600px 0px'});galleryObserver.observe(document.querySelector('.projects-section'));
let lenis,scene,loading=false,disposed=false,inView=true,buildTimeline,idleHandle=0;

// ---------- Menu móvel ----------
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#mobile-nav'),outside=[document.querySelector('main'),document.querySelector('footer')];
function closeMenu(restore=false){if(nav.hidden)return;menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Abrir menu');nav.hidden=true;document.body.classList.remove('menu-open');outside.forEach(el=>el.inert=false);lenis?.start();if(restore)menu.focus();}
function openMenu(){nav.hidden=false;menu.setAttribute('aria-expanded','true');menu.setAttribute('aria-label','Fechar menu');document.body.classList.add('menu-open');outside.forEach(el=>el.inert=true);lenis?.stop();nav.querySelector('a').focus();}
listen(menu,'click',()=>nav.hidden?openMenu():closeMenu(true));
nav.querySelectorAll('a').forEach(link=>listen(link,'click',()=>closeMenu(false)));
listen(document,'keydown',event=>{
  if(nav.hidden)return;
  if(event.key==='Escape'){event.preventDefault();closeMenu(true);}
  if(event.key==='Tab'){const items=[menu,...nav.querySelectorAll('a')],first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}
});
listen(document,'click',event=>{if(!nav.hidden&&!event.target.closest('.topbar'))closeMenu(true);});

// ---------- Estado ativo por seção ----------
const navLinks=[...document.querySelectorAll('.main-nav a')];
const sectionObserver=new IntersectionObserver(entries=>{for(const entry of entries){if(!entry.isIntersecting)continue;navLinks.forEach(link=>link.hash==='#'+entry.target.id?link.setAttribute('aria-current','location'):link.removeAttribute('aria-current'));}},{rootMargin:'-35% 0px -55% 0px'});
document.querySelectorAll('#inicio,#atuacao,#projetos,#processo,#contato').forEach(section=>sectionObserver.observe(section));

// ---------- Construção (estado final = poster; 3D só no desktop capaz) ----------
const states=['Linhas de projeto','Fundação','Estrutura','Fechamentos','Cobertura','Esquadrias','Acabamento'],thresholds=[0,.06,.2,.35,.51,.67,.82];
const state={progress:1,opacity:1},number=document.querySelector('.stage-number'),label=document.querySelector('.stage-name'),notes=[...document.querySelectorAll('.note')];
let lastIndex=-1,lastNotes='';
function paint(){
  root.style.setProperty('--intro-opacity',state.opacity.toFixed(3));root.style.setProperty('--build-progress',state.progress.toFixed(4));scene?.setProgress(state.progress);
  const index=thresholds.reduce((n,value,i)=>state.progress>=value?i:n,0);
  if(index!==lastIndex){lastIndex=index;number.textContent=String(index+1).padStart(2,'0');label.textContent=states[index];hero.dataset.stage=index;}
  const building=root.classList.contains('has-3d')&&state.progress<.985,key=notes.map(n=>building&&index>=Number(n.dataset.from)?1:0).join('');
  if(key!==lastNotes){lastNotes=key;notes.forEach((n,i)=>n.classList.toggle('is-on',key[i]==='1'));}
  // At rest the Cycles poster is shown; the realtime model only appears while building.
  root.classList.toggle('build-active',state.progress<.999||state.opacity<.999);
  if(seq)paintSeq();
}
// ---------- Modo da construção ----------
// '3d': desktop capaz (GLB + Three). 'seq': celular/tablet, 7 quadros WebP do Blender trocados por opacidade.
// null: estático (movimento reduzido, economia de dados, aparelho limitado, ?renderer=static).
// O <head> já reservou o espaço do pin (classes pin-3d/pin-seq), então criar o pin não desloca o layout.
const seqMedia=matchMedia('(max-width:1023px)'),seqHost=document.querySelector('.house-seq');
const seqAllowed=()=>seqMedia.matches&&!motionOff()&&!limited()&&params.get('renderer')!=='static';
const currentMode=()=>!staticOnly()?'3d':seqAllowed()?'seq':null;
let mode,seq=null,seqLoading=false;
function paintSeq(){
  const f=state.progress*6,k=Math.min(6,Math.floor(f)),t=f-k;
  seq.forEach((img,i)=>img.style.opacity=String(i===k?1:i===k+1?t:0));
  poster.style.opacity=String((k===6?1:k===5?t:0)*state.opacity);seqHost.style.opacity=String(state.opacity);
}
async function loadSeq(){
  if(seq||seqLoading||mode!=='seq'||disposed)return;seqLoading=true;
  const frames=[0,1,2,3,4,5].map(i=>Object.assign(new Image(),{src:new URL(`./build-seq/m-${i}.webp`,import.meta.url).href,alt:'',decoding:'async',width:900,height:474}));
  const ok=(await Promise.allSettled(frames.map(img=>img.decode()))).every(r=>r.status==='fulfilled');seqLoading=false;
  if(mode!=='seq'||disposed)return;if(!ok){configure(null);return;}
  frames.forEach(img=>seqHost.append(img));seq=frames;root.classList.add('has-seq');art.dataset.scene='sequence';paint();
}
function removeSeq(){seq?.forEach(img=>img.remove());seq=null;root.classList.remove('has-seq');poster.style.opacity='';seqHost.style.opacity='';}
function frameData(){const [w,h,x0,y0,cw,ch]=(host.dataset.frame||'').split(',').map(Number);return w?{w,h,x0,y0,cw,ch}:undefined;}
const pinDistance=()=>parseFloat(getComputedStyle(story,'::after').height)||0;
// A stage taller than the viewport sticks with its bottom edge visible instead of its top.
const stickOffset=()=>Math.max(0,hero.offsetHeight-innerHeight);
function setStickTop(){hero.style.setProperty('--stick-top',-stickOffset()+'px');}
function configure(next){
  if(next===mode&&(next===null||buildTimeline))return;
  buildTimeline?.scrollTrigger?.kill(true);buildTimeline?.kill();buildTimeline=null;
  if(next!=='3d'){scene?.dispose();scene=null;root.classList.remove('has-3d');}
  if(next!=='seq')removeSeq();
  mode=next;state.progress=1;state.opacity=1;
  root.classList.toggle('pin-3d',next==='3d');root.classList.toggle('pin-seq',next==='seq');root.classList.toggle('static-scene',!next);
  art.dataset.scene=next?'poster':'static';
  if(next){
    buildTimeline=gsap.timeline({onUpdate:()=>{paint();if(buildTimeline?.scrollTrigger?.progress>0)intent();},scrollTrigger:{trigger:story,start:()=>'top top-='+stickOffset(),end:()=>'+='+Math.round(pinDistance()),scrub:next==='3d'?.6:.5,invalidateOnRefresh:true,onRefreshInit:setStickTop}});
    buildTimeline.to(state,{opacity:0,duration:.05,ease:'none'},.01).set(state,{progress:0},.065).to(state,{opacity:1,duration:.05,ease:'none'},.07).to(state,{progress:1,duration:.8,ease:'none'},.1).to({},{duration:.1});
  }
  paint();ScrollTrigger.refresh();
}
function fallback(){configure(null);}
async function loadScene(){
  if(loading||scene||mode!=='3d'||disposed||!inView)return;loading=true;art.dataset.scene='loading';
  try{
    const {createHouseScene}=await import(new URL('./house-scene.js',import.meta.url).href);if(disposed||mode!=='3d')return;
    const next=await createHouseScene(host,{lowPower:(navigator.hardwareConcurrency||8)<=4,frame:frameData(),onUnavailable:fallback});
    if(disposed||mode!=='3d'){next.dispose();return;}
    scene=next;scene.setProgress(state.progress,true);scene.setVisible(inView);root.classList.add('has-3d');art.dataset.scene='ready';paint();
  }catch(error){art.dataset.reason=error.message;fallback();}finally{loading=false;}
}
// No WebGL/GLB on first paint: desktop 3D loads on first intent (pointer over hero, wheel, key, scroll); phone frames also on idle.
function scheduleScene(){if(idleHandle||mode!=='seq')return;const run=()=>{idleHandle=0;mode==='3d'?loadScene():loadSeq();};const idle=()=>window.requestIdleCallback?requestIdleCallback(run,{timeout:2000}):run();idleHandle=setTimeout(idle,1500);}
const intent=()=>mode==='3d'?loadScene():loadSeq();
listen(window,'wheel',intent,{passive:true,once:true});
listen(window,'touchstart',intent,{passive:true,once:true});
listen(window,'keydown',event=>{if(['PageDown','ArrowDown','Space','End'].includes(event.code)&&nav.hidden)intent();});
listen(hero,'pointermove',event=>{if(mode!=='3d')return;if(!scene){loadScene();return;}scene.setPointer((event.clientX/innerWidth-.5)*2,(event.clientY/innerHeight-.5)*2);},{passive:true});
listen(hero,'pointerleave',()=>scene?.setPointer(0,0));
listen(document.querySelector('[data-build-step]'),'click',()=>{if(!buildTimeline)return;const top=buildTimeline.scrollTrigger.end;if(lenis)lenis.scrollTo(top);else scrollTo({top,behavior:motionOff()?'auto':'smooth'});});
const visibility=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;scene?.setVisible(inView);},{rootMargin:'80px'});visibility.observe(hero);
const onCapabilityChange=()=>{closeMenu();configure(currentMode());scheduleScene();};
listen(desktop,'change',onCapabilityChange);listen(seqMedia,'change',onCapabilityChange);listen(reduced,'change',onCapabilityChange);

// ---------- Movimento (GSAP) ----------
const media=gsap.matchMedia();
media.add({motion:'(prefers-reduced-motion:no-preference)',desktop:'(min-width:1024px) and (hover:hover) and (pointer:fine)'},context=>{
  if(!context.conditions.motion||params.get('motion')==='reduce')return;
  const ease='power3.out';
  // Saída do hero: a casa recua e a laje grafite sobe por cima.
  gsap.to('.hero-art',{scale:.9,y:-36,opacity:.5,ease:'none',scrollTrigger:{trigger:'.intro-band',start:'top bottom',end:'top 30%',scrub:true}});
  gsap.to('.hero-monument',{xPercent:-6,ease:'none',scrollTrigger:{trigger:'.intro-band',start:'top bottom',end:'top top',scrub:true}});
  // Below-the-fold reveals are set up after first paint (idle), off the LCP critical path.
  const later=window.requestIdleCallback?requestIdleCallback(()=>context.add(()=>{
  // Revelações discretas.
  gsap.utils.toArray('.intro-inner,.section-head,.projects-head,.process-title>*,.contact-inner>*,.footer-top>*').forEach(el=>gsap.from(el,{y:24,opacity:0,duration:.9,ease,clearProps:'transform,opacity',scrollTrigger:{trigger:el,start:'top 90%',once:true}}));
  gsap.from('.service-line',{y:32,opacity:0,duration:.9,stagger:.08,ease,clearProps:'transform,opacity',scrollTrigger:{trigger:'.service-rail',start:'top 85%',once:true}});
  // Linhas de projeto que se desenham.
  const wire=document.querySelector('.service-wire path');if(wire){wire.setAttribute('pathLength','1');gsap.fromTo(wire,{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,ease:'none',scrollTrigger:{trigger:'.service-rail',start:'top 80%',end:'bottom 60%',scrub:true}});}
  gsap.fromTo('.process-steps',{'--process-line':0},{'--process-line':1,ease:'none',scrollTrigger:{trigger:'.process-steps',start:'top 80%',end:'bottom 55%',scrub:true}});
  // Revelação de imagem por máscara.
  gsap.from('.project-item figure',{clipPath:'inset(10% 6% 10% 6% round 40px)',duration:1.2,ease,stagger:.1,clearProps:'clipPath',scrollTrigger:{trigger:'.project-viewport',start:'top 85%',once:true}});
  gsap.from('.process-plan',{clipPath:'inset(14% 14% 14% 14% round 40px)',duration:1.2,ease,clearProps:'clipPath',scrollTrigger:{trigger:'.process-plan',start:'top 85%',once:true}});
  if(context.conditions.desktop)gsap.fromTo('.process-plan img',{yPercent:4},{yPercent:-4,ease:'none',scrollTrigger:{trigger:'.process-plan',start:'top bottom',end:'bottom top',scrub:true}});
  }),{timeout:1500}):0;
  // Lenis: só desktop com ponteiro fino, um único ticker (GSAP) para Lenis e ScrollTrigger.
  let tick,sync;
  if(context.conditions.desktop&&!limited()){
    lenis=new Lenis({duration:.9,smoothWheel:true,syncTouch:false,anchors:true});
    sync=()=>ScrollTrigger.update();tick=time=>lenis?.raf(time*1000);lenis.on('scroll',sync);gsap.ticker.add(tick);gsap.ticker.lagSmoothing(0);root.dataset.scrollEngine='lenis-desktop';
  }
  return()=>{if(later)cancelIdleCallback(later);if(tick){gsap.ticker.remove(tick);lenis?.off('scroll',sync);lenis?.destroy();lenis=null;}root.dataset.scrollEngine='native';};
});

configure(currentMode());
// site.js is imported after load (see index.html); still handle an early import.
const afterLoad=()=>{ScrollTrigger.refresh();scheduleScene();};if(document.readyState==='complete')afterLoad();else listen(window,'load',afterLoad,{once:true});
function teardown(){disposed=true;closeMenu();lifetime.abort();media.revert();buildTimeline?.scrollTrigger?.kill();buildTimeline?.kill();ScrollTrigger.getAll().forEach(t=>t.kill());visibility.disconnect();sectionObserver.disconnect();galleryObserver.disconnect();gallery.destroy();scene?.dispose();removeSeq();clearTimeout(idleHandle);}
listen(window,'pagehide',event=>{if(event.persisted){scene?.setVisible(false);lenis?.stop();return;}teardown();});
listen(window,'pageshow',event=>{if(event.persisted){scene?.setVisible(inView);lenis?.start();ScrollTrigger.refresh();}});
