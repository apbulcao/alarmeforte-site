/* ===========================================
   ALARMEFORTE — main.js
   =========================================== */

'use strict';

// ===========================
// NAVBAR — scroll behavior
// ===========================
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });


// ===========================
// MOBILE MENU
// ===========================
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  hamburger.classList.toggle('active', isOpen);
  hamburger.setAttribute('aria-expanded', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

// Close on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  });
});

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && navLinks.classList.contains('open')) {
    navLinks.classList.remove('open');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
});


// ===========================
// REVEAL ON SCROLL
// ===========================
const revealEls = document.querySelectorAll('.reveal');

// Hero elements animate immediately on load
const heroReveals = document.querySelectorAll('.hero .reveal');
heroReveals.forEach((el, i) => {
  const delay = [0, 120, 250, 400, 560][i] || 0;
  setTimeout(() => el.classList.add('visible'), delay);
});

// All other elements use IntersectionObserver
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Stagger cards/items within the same parent
      const parent = entry.target.closest('.services-grid, .features-grid, .steps-grid, .stats-grid');
      if (parent) {
        const siblings = Array.from(parent.querySelectorAll('.reveal:not(.visible)'));
        const idx = siblings.indexOf(entry.target);
        setTimeout(() => entry.target.classList.add('visible'), idx * 70);
      } else {
        entry.target.classList.add('visible');
      }
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -48px 0px'
});

revealEls.forEach(el => {
  if (!el.closest('.hero')) revealObserver.observe(el);
});


// ===========================
// COUNTER ANIMATION
// ===========================
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  if (!target) return;

  const duration = 1800;
  const frameRate = 1000 / 60;
  const totalFrames = Math.round(duration / frameRate);
  let frame = 0;

  // Ease out cubic
  const easeOut = t => 1 - Math.pow(1 - t, 3);

  const timer = setInterval(() => {
    frame++;
    const progress = easeOut(frame / totalFrames);
    const current = Math.round(progress * target);

    el.textContent = current >= 1000
      ? current.toLocaleString('pt-BR')
      : current.toString();

    if (frame >= totalFrames) {
      el.textContent = target >= 1000
        ? target.toLocaleString('pt-BR')
        : target.toString();
      clearInterval(timer);
    }
  }, frameRate);
}

let countersStarted = false;
const statsSection = document.getElementById('numeros');

if (statsSection) {
  const counterObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !countersStarted) {
      countersStarted = true;
      document.querySelectorAll('.stat-number[data-target]').forEach(el => {
        animateCounter(el);
      });
    }
  }, { threshold: 0.25 });

  counterObserver.observe(statsSection);
}


// ===========================
// CONTACT FORM (FORMSPREE)
// ===========================
const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');
const submitBtn   = document.getElementById('submitBtn');

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Check if Formspree ID is configured
    if (contactForm.action.includes('YOUR_FORMSPREE_ID')) {
      alert('Atenção: configure o Formspree antes de usar o formulário. Veja o comentário no index.html.');
      return;
    }

    const btnText    = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');

    btnText.hidden    = true;
    btnLoading.hidden = false;
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.75';

    try {
      const response = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });

      if (response.ok) {
        contactForm.hidden = true;
        formSuccess.hidden = false;
        formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || 'Erro ao enviar');
      }
    } catch (err) {
      console.error('Form error:', err);
      btnText.hidden    = false;
      btnLoading.hidden = true;
      submitBtn.disabled = false;
      submitBtn.style.opacity = '';
      alert('Ocorreu um erro ao enviar. Por favor, tente novamente ou ligue: (21) 3890-4336.');
    }
  });
}


// ===========================
// SMOOTH ANCHOR SCROLL
// (accounts for fixed navbar height)
// ===========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const id = anchor.getAttribute('href');
    if (id === '#' || id === '#!') return;
    const target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    const offset = navbar.offsetHeight + 12;
    const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});


// ===========================
// NAV DROPDOWN
// ===========================
(function () {
  var wrappers = document.querySelectorAll('.nav-dropdown-wrapper');

  wrappers.forEach(function (wrapper) {
    var toggle = wrapper.querySelector('.nav-dropdown-toggle');
    var menu = wrapper.querySelector('.nav-dropdown-menu');

    if (!toggle || !menu) return;

    // Desktop: hover
    wrapper.addEventListener('mouseenter', function () {
      wrapper.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
    });
    wrapper.addEventListener('mouseleave', function () {
      wrapper.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });

    // Click (mobile e teclado)
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = wrapper.classList.contains('open');
      // Fecha todos
      wrappers.forEach(function (w) {
        w.classList.remove('open');
        var t = w.querySelector('.nav-dropdown-toggle');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
      // Abre este se estava fechado
      if (!isOpen) {
        wrapper.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // Fecha dropdown ao clicar fora
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown-wrapper')) {
      wrappers.forEach(function (w) {
        w.classList.remove('open');
        var t = w.querySelector('.nav-dropdown-toggle');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });
})();
