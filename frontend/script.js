document.addEventListener('DOMContentLoaded', function () {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  const pathName = window.location.pathname.split('/').pop();

  document.querySelectorAll('.nav-link').forEach((link) => {
    const href = link.getAttribute('href').split('/').pop();
    let isActive = href === pathName;
    if (!isActive) {
      if (pathName === '') {
        if (href === 'index.html') {
          isActive = true;
        }
      }
    }
    if (isActive) {
      link.classList.add('active');
    }
  });

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      const isOpen = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
  }

  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
});