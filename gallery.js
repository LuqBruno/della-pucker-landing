import EmblaCarousel from 'embla-carousel';
export function initProjectGallery() {
  const viewport = document.querySelector('.project-viewport');
  if (!viewport) return { destroy() {} };
  const section = viewport.closest('.projects-section'), reduced = matchMedia('(prefers-reduced-motion: reduce)'), abort = new AbortController();
  const api = EmblaCarousel(viewport, { align: 'start', containScroll: 'trimSnaps', loop: false, duration: reduced.matches ? 0 : 30, dragThreshold: 8 });
  viewport.classList.add('embla-ready'); viewport.dataset.engine = 'embla';
  const arrows = [...section.querySelectorAll('[data-project-scroll]')], dots = [...section.querySelectorAll('[data-project-index]')];
  const position = section.querySelector('.gallery-position'), progress = section.querySelector('.gallery-progress span');
  const listen = (target, type, fn) => target.addEventListener(type, fn, { signal: abort.signal });
  const slides = api.slideNodes(), total = slides.length, pad = n => String(n).padStart(2, '0');
  slides.forEach((slide, index) => { slide.setAttribute('role', 'group'); slide.setAttribute('aria-roledescription', 'slide'); slide.setAttribute('aria-label', `${index + 1} de ${total}`); });
  function update() {
    const index = api.selectedScrollSnap(), snaps = api.scrollSnapList().length;
    viewport.dataset.position = String(index + 1);
    progress?.style.setProperty('transform', `scaleX(${(index + 1) / snaps})`);
    position.textContent = `${pad(index + 1)} / ${pad(snaps)}`;
    arrows.forEach(button => button.disabled = Number(button.dataset.projectScroll) < 0 ? !api.canScrollPrev() : !api.canScrollNext());
    dots.forEach((dot, i) => i === index ? dot.setAttribute('aria-current', 'true') : dot.removeAttribute('aria-current'));
    slides.forEach((slide, i) => slide.classList.toggle('is-selected', i === index));
  }
  const jump = () => reduced.matches;
  arrows.forEach(button => listen(button, 'click', () => Number(button.dataset.projectScroll) < 0 ? api.scrollPrev(jump()) : api.scrollNext(jump())));
  dots.forEach(dot => listen(dot, 'click', () => api.scrollTo(Number(dot.dataset.projectIndex), jump())));
  listen(viewport, 'keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.target !== viewport && event.target.closest('a')) return;
    const moves = { ArrowLeft: () => api.scrollPrev(jump()), ArrowRight: () => api.scrollNext(jump()), Home: () => api.scrollTo(0, jump()), End: () => api.scrollTo(api.scrollSnapList().length - 1, jump()) };
    if (moves[event.key]) { event.preventDefault(); moves[event.key](); }
  });
  // Keyboard focus moving into a slide link brings that slide into view.
  slides.forEach((slide, i) => listen(slide, 'focusin', () => { if (api.selectedScrollSnap() !== i) api.scrollTo(i, true); viewport.scrollLeft = 0; }));
  listen(reduced, 'change', () => api.reInit({ duration: reduced.matches ? 0 : 30 }));
  api.on('select', update).on('reInit', update).on('pointerDown', () => viewport.classList.add('is-dragging')).on('pointerUp', () => viewport.classList.remove('is-dragging'));
  update();
  return { destroy() { abort.abort(); api.destroy(); viewport.classList.remove('embla-ready'); slides.forEach(slide => slide.classList.remove('is-selected')); } };
}
