(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reveals = document.querySelectorAll('.reveal');
  if (reduced) reveals.forEach((el) => el.classList.add('visible'));
  else {
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
    }), { threshold: 0.12 });
    reveals.forEach((el) => observer.observe(el));
  }

  const filters = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('[data-category]');
  filters.forEach((button) => button.addEventListener('click', () => {
    filters.forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    cards.forEach((card) => {
      const visible = button.dataset.filter === 'all' || card.dataset.category.includes(button.dataset.filter);
      card.hidden = !visible;
    });
  }));

  const header = document.querySelector('[data-header]');
  if (header) window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 24), { passive: true });
  const toTop = document.querySelector('[data-to-top]');
  if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));
  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
