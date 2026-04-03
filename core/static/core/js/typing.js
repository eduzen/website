// Typing animation for home page hero — HTMX-aware
(function() {
  var typingTimeout = null;
  var running = false;

  var TYPE_SPEED = 100;
  var DELETE_SPEED = 80;

  function getNameEl() {
    var el = document.getElementById('typed-name');
    return el && el.isConnected ? el : null;
  }

  function setName(nameEl, text) {
    if (!nameEl || !nameEl.isConnected) return;
    nameEl.innerHTML = '';
    var parts = text.split('\n');
    parts.forEach(function(part, i) {
      nameEl.appendChild(document.createTextNode(part));
      if (i < parts.length - 1) {
        nameEl.appendChild(document.createElement('br'));
      }
    });
  }

  function scheduleNext(fn, delay) {
    typingTimeout = setTimeout(fn, delay);
  }

  function typeChars(nameEl, text, from, callback) {
    var i = from;
    function next() {
      if (!running || !nameEl.isConnected) return;
      if (i <= text.length) {
        setName(nameEl, text.slice(0, i));
        i++;
        scheduleNext(next, TYPE_SPEED);
      } else {
        callback();
      }
    }
    next();
  }

  function deleteLine(nameEl, line1, line2, callback) {
    var len = line2.length;
    function next() {
      if (!running || !nameEl.isConnected) return;
      if (len > 0) {
        len--;
        setName(nameEl, line1 + '\n' + line2.slice(0, len));
        scheduleNext(next, DELETE_SPEED);
      } else {
        setName(nameEl, line1);
        scheduleNext(callback, 100);
      }
    }
    next();
  }

  function deleteWord(nameEl, callback) {
    function next() {
      if (!running || !nameEl.isConnected) return;
      var text = nameEl.textContent;
      if (text.length > 0) {
        setName(nameEl, text.slice(0, -1));
        scheduleNext(next, DELETE_SPEED);
      } else {
        callback();
      }
    }
    next();
  }

  function runCycle() {
    var nameEl = getNameEl();
    if (!nameEl || !running) return;

    typeChars(nameEl, 'Eduardo', 0, function() {
      if (!running) return;
      scheduleNext(function() {
        if (!running) return;
        setName(nameEl, 'Eduardo\n');
        typeChars(nameEl, 'Eduardo\nEnriquez', 'Eduardo\n'.length, function() {
          if (!running) return;
          scheduleNext(function() {
            if (!running) return;
            deleteLine(nameEl, 'Eduardo', 'Enriquez', function() {
              if (!running) return;
              deleteWord(nameEl, function() {
                if (!running) return;
                scheduleNext(function() {
                  if (!running) return;
                  typeChars(nameEl, 'eduzen', 0, function() {
                    if (!running) return;
                    scheduleNext(runCycle, 3000);
                  });
                }, 300);
              });
            });
          }, 1500);
        });
      }, 400);
    });
  }

  function startTyping() {
    stopTyping();
    if (!getNameEl()) return;
    running = true;
    scheduleNext(runCycle, 800);
  }

  function stopTyping() {
    running = false;
    if (typingTimeout) {
      clearTimeout(typingTimeout);
      typingTimeout = null;
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    startTyping();
  });

  document.body.addEventListener('htmx:beforeSwap', stopTyping);

  document.body.addEventListener('htmx:afterSwap', function() {
    startTyping();
  });
})();
