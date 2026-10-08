document.addEventListener('DOMContentLoaded', () => {
  const active = document.querySelector('.nav-link.active');
  if (active) {
    active.setAttribute('aria-current', 'page');
  }
});
