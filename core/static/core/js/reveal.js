// Scroll reveal animation — HTMX-aware
(function() {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  function observeRevealElements(root) {
    var elements = (root || document).querySelectorAll('.reveal:not(.visible)');
    elements.forEach(function(el) { observer.observe(el); });
  }

  document.addEventListener('DOMContentLoaded', function() {
    observeRevealElements();
  });

  document.body.addEventListener('htmx:afterSwap', function(evt) {
    observeRevealElements(evt.detail.target);
  });
})();
