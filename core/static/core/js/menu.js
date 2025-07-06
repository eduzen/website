document.addEventListener("DOMContentLoaded", function() {
  function handleDropdownBehavior() {
    document.addEventListener("click", function(event) {
      const dropdown = document.getElementById("language-dropdown");
      const button = document.getElementById("language-button");

      // Hide language dropdown if clicked outside
      if (dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target) && !dropdown.classList.contains("hidden")) {
        dropdown.classList.add("hidden");
      }
    });
  }

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
    // Show loading indicator on HTMX requests
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
      const indicator = document.getElementById('loadingIndicator');
      if (indicator) {
        indicator.classList.remove('scale-x-0');
        indicator.classList.add('scale-x-100');
      }
    });

    // Hide loading indicator when request completes
    document.body.addEventListener('htmx:afterRequest', function(evt) {
      const indicator = document.getElementById('loadingIndicator');
      if (indicator) {
        setTimeout(() => {
          indicator.classList.remove('scale-x-100');
          indicator.classList.add('scale-x-0');
        }, 200);
      }
    });

    // Handle HTMX errors
    document.body.addEventListener('htmx:responseError', function(evt) {
      console.error('HTMX Request failed:', evt.detail);
      const indicator = document.getElementById('loadingIndicator');
      if (indicator) {
        indicator.classList.remove('scale-x-100', 'bg-blue-500');
        indicator.classList.add('scale-x-0', 'bg-red-500');
        setTimeout(() => {
          indicator.classList.remove('bg-red-500');
          indicator.classList.add('bg-blue-500');
        }, 2000);
      }
    });

    // Update active navigation state after HTMX navigation
    document.body.addEventListener('htmx:afterSettle', function(evt) {
      // Small delay to ensure URL has been updated by hx-push-url
      setTimeout(() => {
        updateActiveNavigation();
      }, 10);
    });
  }

  // Initialize functions
  handleDropdownBehavior();
  handleHTMXEvents();

  // Update active state on initial page load
  updateActiveNavigation();

  // Also listen for URL changes (for hx-push-url)
  window.addEventListener('popstate', function() {
    updateActiveNavigation();
  });
});
