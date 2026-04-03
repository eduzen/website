document.addEventListener("DOMContentLoaded", function() {
  function updateActiveNavigation() {
    const currentPath = window.location.pathname;

    // Remove active-link class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.remove('active-link');

      // Get the href attribute
      const href = link.getAttribute('href') || '';

      // Check if current path matches the link
      if (href === currentPath) {
        // Exact match
        link.classList.add('active-link');
      } else if (href !== '/' && href !== '' && href.endsWith('/') && currentPath.startsWith(href)) {
        // For section pages, match if current path starts with the href
        link.classList.add('active-link');
      }
    });
  }

  function handleHTMXEvents() {
    var indicator = document.getElementById('loadingIndicator');

    document.body.addEventListener('htmx:beforeRequest', function() {
      if (indicator) {
        indicator.classList.remove('scale-x-0');
        indicator.classList.add('scale-x-100');
      }
    });

    document.body.addEventListener('htmx:afterRequest', function() {
      if (indicator) {
        setTimeout(function() {
          indicator.classList.remove('scale-x-100');
          indicator.classList.add('scale-x-0');
        }, 200);
      }
    });

    document.body.addEventListener('htmx:responseError', function(evt) {
      console.error('HTMX Request failed:', evt.detail);
      if (indicator) {
        indicator.classList.remove('scale-x-100');
        indicator.classList.add('scale-x-0');
        indicator.style.background = 'var(--error)';
        setTimeout(function() {
          indicator.style.background = '';
        }, 2000);
      }
    });

    document.body.addEventListener('htmx:afterSettle', function() {
      if (window.location.pathname !== lastPath) {
        lastPath = window.location.pathname;
        updateActiveNavigation();
      }
    });
  }

  var lastPath = window.location.pathname;

  // Initialize functions
  handleHTMXEvents();

  // Update active state on initial page load
  updateActiveNavigation();

  // Also listen for URL changes (for hx-push-url)
  window.addEventListener('popstate', function() {
    updateActiveNavigation();
  });
});
