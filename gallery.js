import EmblaCarousel from 'embla-carousel';
export function initProjectGallery() {
  const viewport = document.querySelector('.project-viewport');
  if (!viewport) return { destroy() {} };
  const section = viewport.closest('.projects-section'), reduced = matchMedia('(prefers-reduced-motion: reduce)'), abort = new AbortController();
  const api = EmblaCarousel(viewport, { align: 'start', containScroll: 'trimSnaps', loop: false, duration: reduced.matches ? 0 : 28, dragThreshold: 8 });
  viewport.classList.add('embla-ready'); viewport.dataset.engine = 'embla';
  viewport.setAttribute('aria-roledescription','carrossel');
  const arrows = [...section.querySelectorAll('[data-project-scroll]')], dots = [...section.querySelectorAll('[data-project-index]')], position = section.querySelector('.gallery-position');
  const listen = (target, type, fn) => target.addEventListener(type, fn, { signal: abort.signal });
  api.slideNodes().forEach((slide, index) => { slide.setAttribute('role', 'group'); slide.setAttribute('aria-label', `${index + 1} de ${api.slideNodes().length}: ${slide.querySelector('h3').textContent}`); });
  function update() {
    const index = api.selectedScrollSnap();
    viewport.dataset.position = String(index + 1);
    section.querySelector('.gallery-progress span')?.style.setProperty('width', `${(index+1)/api.scrollSnapList().length*100}%`);
    position.textContent = `${String(index + 1).padStart(2, '0')} / ${String(api.scrollSnapList().length).padStart(2, '0')}`;
    arrows.forEach(button => button.disabled = Number(button.dataset.projectScroll) < 0 ? !api.canScrollPrev() : !api.canScrollNext());
    dots.forEach((dot, i) => i === index ? dot.setAttribute('aria-current', 'true') : dot.removeAttribute('aria-current'));
  }
  arrows.forEach(button => listen(button, 'click', () => Number(button.dataset.projectScroll) < 0 ? api.scrollPrev(reduced.matches) : api.scrollNext(reduced.matches)));
  dots.forEach(dot => listen(dot, 'click', () => api.scrollTo(Number(dot.dataset.projectIndex), reduced.matches)));
  listen(viewport, 'keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    const moves = { ArrowLeft: () => api.scrollPrev(reduced.matches), ArrowRight: () => api.scrollNext(reduced.matches), Home: () => api.scrollTo(0, reduced.matches), End: () => api.scrollTo(api.scrollSnapList().length - 1, reduced.matches) };
    if (moves[event.key]) { event.preventDefault(); moves[event.key](); }
  });
  listen(reduced, 'change', () => api.reInit({ duration: reduced.matches ? 0 : 28 }));
  api.on('select', update).on('reInit', update); update();
  return { destroy() { abort.abort(); api.destroy(); viewport.classList.remove('embla-ready'); } };
}
