// Typing animation for home page hero — HTMX-aware
(function() {
  var TYPE_SPEED = 100;
  var DELETE_SPEED = 80;
  var START_DELAY = 800;
  var FULL_NAME = 'Eduardo\nEnriquez';

  // Each step types forward to `type`, erases back to `erase`, or waits `pause` ms. The list loops.
  var STEPS = [
    { type: 'Eduardo' },
    { pause: 400 },
    { type: FULL_NAME },
    { pause: 1500 },
    { erase: 'Eduardo' },
    { pause: 100 },
    { erase: '' },
    { pause: 300 },
    { type: 'eduzen' },
    { pause: 3000 }
  ];

  var reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  var timer = null;

  function render(nameEl, text) {
    nameEl.replaceChildren();
    text.split('\n').forEach(function(line, i) {
      if (i > 0) nameEl.appendChild(document.createElement('br'));
      nameEl.appendChild(document.createTextNode(line));
    });
  }

  function animate(nameEl) {
    var text = '';
    var stepIndex = 0;

    function nextStep(delay) {
      stepIndex = (stepIndex + 1) % STEPS.length;
      timer = setTimeout(tick, delay);
    }

    function tick() {
      var step = STEPS[stepIndex];

      if ('pause' in step) {
        nextStep(step.pause);
      } else if ('type' in step) {
        if (!step.type.startsWith(text)) text = '';
        if (text === step.type) return nextStep(0);
        text = step.type.slice(0, text.length + 1);
        render(nameEl, text);
        timer = setTimeout(tick, TYPE_SPEED);
      } else {
        if (text === step.erase) return nextStep(0);
        text = text.slice(0, -1);
        render(nameEl, text);
        timer = setTimeout(tick, DELETE_SPEED);
      }
    }

    timer = setTimeout(tick, START_DELAY);
  }

  function stop() {
    clearTimeout(timer);
    timer = null;
  }

  function start() {
    stop();
    var nameEl = document.getElementById('typed-name');
    if (!nameEl) return;
    if (reducedMotionQuery.matches) {
      render(nameEl, FULL_NAME);
      return;
    }
    animate(nameEl);
  }

  document.addEventListener('DOMContentLoaded', start);
  document.body.addEventListener('htmx:beforeSwap', stop);
  document.body.addEventListener('htmx:afterSwap', start);
  reducedMotionQuery.addEventListener('change', start);
})();
