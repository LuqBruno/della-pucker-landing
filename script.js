import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
import { initProjectGallery } from './gallery.js';
gsap.registerPlugin(ScrollTrigger);
const root=document.documentElement,story=document.querySelector('.hero-scroll'),hero=document.querySelector('#construction-story');
const art=document.querySelector('.hero-art'),host=document.querySelector('.house-canvas'),poster=document.querySelector('.house-poster');
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),desktop=matchMedia('(min-width:901px) and (hover:hover) and (pointer:fine)'),params=new URLSearchParams(location.search);
const limited=()=>navigator.connection?.saveData||/^(slow-)?2g$/.test(navigator.connection?.effectiveType||'')||(navigator.hardwareConcurrency&&navigator.hardwareConcurrency<=2)||(navigator.deviceMemory&&navigator.deviceMemory<=2);
const staticOnly=()=>reduced.matches||params.get('motion')==='reduce'||params.get('renderer')==='static'||!desktop.matches||limited();
root.classList.add('js');
const lifetime=new AbortController(),listen=(target,type,fn,options={})=>target.addEventListener(type,fn,{...options,signal:lifetime.signal});
const message='Olá, gostaria de conversar com a Della & Pucker sobre um projeto. Podem me orientar sobre o orçamento?';
document.querySelectorAll('[data-contact]').forEach(link=>link.href='https://wa.me/554834127737?text='+encodeURIComponent(message));
const gallery=initProjectGallery(),menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#mobile-nav');
let lenis,scene,loading=false,disposed=false,inView=true,buildTimeline,frame=0;
function closeMenu(restore=false){menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Abrir menu');nav.hidden=true;document.body.classList.remove('menu-open');document.querySelector('main').inert=false;document.querySelector('footer').inert=false;lenis?.start();if(restore)menu.focus();}
listen(menu,'click',()=>{if(!nav.hidden){closeMenu(true);return;}nav.hidden=false;menu.setAttribute('aria-expanded','true');menu.setAttribute('aria-label','Fechar menu');document.body.classList.add('menu-open');document.querySelector('main').inert=true;document.querySelector('footer').inert=true;lenis?.stop();nav.querySelector('a').focus();});
nav.querySelectorAll('a').forEach(link=>listen(link,'click',()=>closeMenu(true)));
listen(document,'keydown',event=>{if(nav.hidden)return;if(event.key==='Escape'){event.preventDefault();closeMenu(true);}if(event.key==='Tab'){const items=[menu,...nav.querySelectorAll('a')],first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}});
listen(document,'click',event=>{if(!nav.hidden&&!event.target.closest('.topbar'))closeMenu(true);});
listen(desktop,'change',()=>{closeMenu();if(staticOnly())fallback();else root.classList.remove('static-scene');ScrollTrigger.refresh();});
const sectionObserver=new IntersectionObserver(entries=>{for(const entry of entries){if(!entry.isIntersecting)continue;document.querySelectorAll('.main-nav a').forEach(link=>link.hash==='#'+entry.target.id?link.setAttribute('aria-current','location'):link.removeAttribute('aria-current'));}},{rootMargin:'-15% 0px -60% 0px'});
document.querySelectorAll('#atuacao,#projetos,#processo').forEach(section=>sectionObserver.observe(section));
const states=['Linhas de projeto','Fundação','Estrutura ilustrativa','Fechamentos','Cobertura','Esquadrias','Acabamento'],thresholds=[0,.04,.18,.34,.5,.67,.83];
const state={progress:1,opacity:1},number=document.querySelector('.stage-number'),label=document.querySelector('.stage-name');
function paint(){frame=0;root.style.setProperty('--intro-opacity',state.opacity);root.style.setProperty('--build-progress',state.progress);scene?.setProgress(state.progress,true);const index=thresholds.reduce((n,value,i)=>state.progress>=value?i:n,0);number.textContent=String(index+1).padStart(2,'0');label.textContent=states[index];hero.dataset.stage=index;}
function fallback(){buildTimeline?.scrollTrigger?.kill(true);buildTimeline?.kill();buildTimeline=null;scene?.dispose();scene=null;root.classList.add('static-scene');root.classList.remove('has-3d');poster.hidden=false;art.dataset.scene='static';state.progress=1;state.opacity=1;paint();}
function setupBuild(){if(buildTimeline||staticOnly())return;buildTimeline=gsap.timeline({onUpdate:paint,scrollTrigger:{trigger:story,start:()=> 'top top+='+document.querySelector('.topbar').offsetHeight,end:()=>'+='+Math.min(1100,innerHeight*1.2),pin:hero,pinSpacing:true,scrub:.45,invalidateOnRefresh:true}});buildTimeline.to(state,{opacity:0,duration:.07,ease:'none'},.015).set(state,{progress:0},.085).to(state,{opacity:1,duration:.06,ease:'none'},.12).to(state,{progress:1,duration:.76,ease:'none'},.12).to(art,{scale:.97,y:12,duration:.12,ease:'power2.out'},.88);ScrollTrigger.refresh();}
const media=gsap.matchMedia();
media.add({motion:'(prefers-reduced-motion:no-preference)',desktop:'(min-width:901px) and (hover:hover) and (pointer:fine)'},context=>{
 if(!context.conditions.motion||params.get('motion')==='reduce')return;
 gsap.from('.hero-copy h1,.hero-deck,.hero-copy .primary-cta,.hero-project-link',{y:16,opacity:.85,duration:.9,stagger:.06,ease:'power3.out',clearProps:'transform,opacity'});
 document.querySelectorAll('.section-head,.service-line,.projects-head,.process-title,.contact-inner').forEach(element=>gsap.from(element,{y:20,opacity:.9,duration:.6,ease:'power3.out',clearProps:'transform,opacity',scrollTrigger:{trigger:element,start:'top 92%',once:true}}));
 gsap.fromTo('.process-title',{'--process-line':0},{'--process-line':1,duration:.9,ease:'power3.out',scrollTrigger:{trigger:'.process',start:'top 85%',once:true}});
 let tick,sync;
 if(context.conditions.desktop&&!limited()){lenis=new Lenis({duration:.85,smoothWheel:true,syncTouch:false,anchors:{offset:-document.querySelector('.topbar').offsetHeight}});sync=()=>ScrollTrigger.update();tick=time=>lenis?.raf(time*1000);lenis.on('scroll',sync);gsap.ticker.add(tick);root.dataset.scrollEngine='lenis-desktop';}
 return()=>{if(tick){gsap.ticker.remove(tick);lenis?.off('scroll',sync);lenis?.destroy();lenis=null;}root.dataset.scrollEngine='native';};
});
async function loadScene(){if(loading||scene||staticOnly()||disposed||!inView)return;loading=true;art.dataset.scene='loading';
 try{const {createHouseScene}=await import(new URL('./house-scene.js',import.meta.url).href);if(disposed||staticOnly())return;const next=await createHouseScene(host,{lowPower:navigator.hardwareConcurrency<=4,onUnavailable:fallback});if(disposed||staticOnly()){next.dispose();return;}scene=next;scene.setProgress(state.progress,true);scene.setVisible(inView);root.classList.remove('static-scene');root.classList.add('has-3d');art.dataset.scene='ready';setupBuild();paint();}
 catch(error){fallback();art.dataset.reason=error.message;}finally{loading=false;}
}
// No WebGL or GLB cost on first paint. Desktop construction loads only on intent.
listen(window,'wheel',()=>loadScene(),{passive:true});
listen(window,'keydown',event=>{if(['PageDown','ArrowDown','Space'].includes(event.code)&&nav.hidden)loadScene();});
listen(hero,'pointerdown',()=>loadScene(),{passive:true});
listen(hero,'pointermove',event=>{if(!scene||staticOnly())return;scene.setPointer?.((event.clientX/innerWidth-.5)*2,(event.clientY/innerHeight-.5)*2);},{passive:true});
listen(hero,'pointerleave',()=>scene?.setPointer?.(0,0));
listen(document.querySelector('[data-build-step]'),'click',async()=>{await loadScene();if(!buildTimeline)return;const top=buildTimeline.scrollTrigger.end;if(lenis)lenis.scrollTo(top);else scrollTo({top,behavior:staticOnly()?'auto':'smooth'});});
const visibility=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;scene?.setVisible(inView);},{rootMargin:'40px'});visibility.observe(hero);
listen(reduced,'change',()=>{if(staticOnly())fallback();else root.classList.remove('static-scene');});
if(staticOnly())fallback();else{art.dataset.scene='poster';paint();}
listen(window,'load',()=>ScrollTrigger.refresh(),{once:true});
listen(window,'pagehide',event=>{if(event.persisted){scene?.setVisible(false);lenis?.stop();return;}disposed=true;closeMenu();lifetime.abort();media.revert();buildTimeline?.scrollTrigger?.kill();buildTimeline?.kill();visibility.disconnect();sectionObserver.disconnect();gallery.destroy();scene?.dispose();cancelAnimationFrame(frame);});
listen(window,'pageshow',event=>{if(event.persisted){scene?.setVisible(inView);lenis?.start();ScrollTrigger.refresh();}});
