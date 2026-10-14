// Homepage-only background studies. Each visit owns one animation and its listeners.
(function() {
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  var selected = 'tide';
  var cleanup = function() {};
  var colors = ['194, 105, 45', '232, 168, 124', '92, 107, 79'];

  try {
    var saved = sessionStorage.getItem('home-atmosphere');
    if (['original', 'tide', 'light', 'bloom'].includes(saved)) selected = saved;
  } catch (err) { /* The previews also work without browser storage. */ }

  function start() {
    cleanup();
    var canvas = document.getElementById('home-atmosphere');
    var picker = document.querySelector('.atmosphere-picker');
    if (!canvas || !picker) return;
    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var events = new AbortController();
    var options = { signal: events.signal };
    var width = 0;
    var height = 0;
    var frame = null;
    var lastTime = null;
    var time = 0;
    var pointer = { x: 0.5, strength: 0 };
    var target = { x: 0.5, strength: 0 };
    var blooms = [];
    var nextBloom = 2;
    var lastPointerBloom = -10;

    function wash(x, y, radius, color, opacity) {
      var gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
      gradient.addColorStop(0, 'rgba(' + color + ', ' + opacity + ')');
      gradient.addColorStop(1, 'rgba(' + color + ', 0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    function tide() {
      colors.forEach(function(color, layer) {
        ctx.beginPath();
        ctx.moveTo(0, height);
        for (var x = 0; x <= width + 8; x += 8) {
          var u = x / width;
          // Unequal frequencies create broad, evolving contours without a sliding tile.
          var swell = Math.sin(u * 6.2 + time * 0.19 + layer * 1.9) * 0.065
            + Math.sin(u * 10.7 - time * 0.13 + layer) * 0.025
            + Math.cos(u * 3.4 + time * 0.11) * 0.035;
          var distance = (u - pointer.x) / 0.15;
          var lift = Math.exp(-distance * distance) * pointer.strength * 0.1;
          ctx.lineTo(x, height * (0.48 + layer * 0.16 + swell - lift));
        }
        ctx.lineTo(width, height);
        ctx.closePath();
        ctx.fillStyle = 'rgba(' + color + ', ' + [0.095, 0.1, 0.08][layer] + ')';
        ctx.fill();
      });
    }

    function light() {
      colors.forEach(function(color, layer) {
        var x = width * (0.2 + layer * 0.29 + Math.sin(time * 0.09 + layer * 2.4) * 0.12);
        x += (pointer.x * width - x) * pointer.strength * 0.18;
        var y = height * (0.8 + Math.sin(time * 0.13 + layer * 1.7) * 0.12);
        ctx.save();
        ctx.scale(1, 0.65);
        wash(x, y / 0.65, Math.max(width * 0.34, height), color, 0.15);
        ctx.restore();
      });
    }

    function addBloom(x) {
      blooms.push({ x: x, y: 0.66 + Math.random() * 0.22, born: time, color: colors[2], life: 8 });
      if (blooms.length > 6) blooms.shift();
    }

    function bloom() {
      wash(width * 0.3, height * 1.1, Math.max(width * 0.45, height), colors[1], 0.1);
      var visible = reducedMotion.matches
        ? [{ x: 0.68, y: 0.8, born: time - 4, color: colors[2], life: 8 }]
        : blooms;
      visible.forEach(function(item) {
        var progress = (time - item.born) / item.life;
        var opacity = Math.sin(progress * Math.PI) * 0.16;
        var radius = (0.2 + progress * 0.8) * Math.min(width * 0.3, 420);
        var x = item.x * width;
        var y = item.y * height - progress * height * 0.08;
        wash(x, y, radius * 1.4, item.color, opacity * 0.65);
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(1, 0.32);
        [1, 0.72].forEach(function(scale) {
          ctx.beginPath();
          ctx.arc(0, 0, radius * scale, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(' + item.color + ', ' + opacity + ')';
          ctx.lineWidth = 1;
          ctx.stroke();
        });
        ctx.restore();
      });
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);
      if (selected === 'tide') tide();
      if (selected === 'light') light();
      if (selected === 'bloom') bloom();
    }

    function tick(now) {
      frame = requestAnimationFrame(tick);
      if (lastTime !== null && now - lastTime < 32) return;
      var delta = lastTime === null ? 0 : Math.min((now - lastTime) / 1000, 0.08);
      lastTime = now;
      time += delta;
      var ease = 1 - Math.exp(-delta * 2.2);
      pointer.x += (target.x - pointer.x) * ease;
      pointer.strength += (target.strength - pointer.strength) * ease;
      if (selected === 'bloom') {
        blooms = blooms.filter(function(item) { return time - item.born < item.life; });
        if (time >= nextBloom) {
          addBloom(0.12 + Math.random() * 0.76);
          nextBloom = time + 5 + Math.random() * 7;
        }
        if (target.strength > 0.2 && time - lastPointerBloom > 2.5) {
          addBloom(pointer.x);
          lastPointerBloom = time;
        }
      }
      draw();
    }

    function resume() {
      cancelAnimationFrame(frame);
      frame = null;
      lastTime = null;
      if (reducedMotion.matches) {
        pointer.strength = 0;
        target.strength = 0;
      }
      draw();
      if (!reducedMotion.matches && !document.hidden && selected !== 'original') {
        frame = requestAnimationFrame(tick);
      }
    }

    function resize() {
      if (selected === 'original') return;
      var rect = canvas.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      var ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      draw();
    }

    function select() {
      canvas.hidden = selected === 'original';
      document.body.classList.toggle('home-atmosphere-active', selected !== 'original');
      picker.querySelectorAll('button').forEach(function(button) {
        button.setAttribute('aria-pressed', String(button.dataset.atmosphere === selected));
      });
      blooms = [];
      nextBloom = time + 1;
      resize();
      resume();
    }

    picker.addEventListener('click', function(event) {
      var button = event.target.closest('button[data-atmosphere]');
      if (!button) return;
      selected = button.dataset.atmosphere;
      try { sessionStorage.setItem('home-atmosphere', selected); } catch (err) { /* Optional. */ }
      select();
    }, options);
    window.addEventListener('pointermove', function(event) {
      if (!finePointer.matches || reducedMotion.matches || event.pointerType === 'touch') return;
      target.x = event.clientX / window.innerWidth;
      target.strength = Math.max(0, Math.min(1, (event.clientY / window.innerHeight - 0.2) / 0.65));
    }, options);
    document.documentElement.addEventListener('pointerleave', function() { target.strength = 0; }, options);
    window.addEventListener('blur', function() { target.strength = 0; }, options);
    window.addEventListener('resize', resize, options);
    document.addEventListener('visibilitychange', resume, options);
    reducedMotion.addEventListener('change', resume, options);

    picker.hidden = false;
    select();
    cleanup = function() {
      cancelAnimationFrame(frame);
      events.abort();
      document.body.classList.remove('home-atmosphere-active');
      picker.hidden = true;
      canvas.hidden = true;
    };
  }

  document.addEventListener('DOMContentLoaded', start);
  document.body.addEventListener('htmx:beforeSwap', function(event) {
    if (event.detail.target.id === 'content' && event.detail.shouldSwap) cleanup();
  });
  document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'content') start();
  });
})();
