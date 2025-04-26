function cleanLoadingIndicator() {
  const loadingIndicator = document.getElementById('loadingIndicator');
  if (loadingIndicator) {
    loadingIndicator.style.transform = 'scaleX(0)'; // Reset the indicator
  }
}

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

  function updateActiveLink(event) {
    if (!event || !event.detail || !event.detail.pathInfo || !event.detail.pathInfo.requestPath) {
      return; // Exit if no proper event details are provided
    }

    const navLinks = document.querySelectorAll("#main-navbar .nav-link");
    navLinks.forEach(link => {
      // If the href in the id of the link matches the current path
      if (event.detail.pathInfo.requestPath.includes(link.id)) {
        link.classList.add('active-link');
      } else {
        link.classList.remove('active-link');
      }
    });
  }

  function handleHTMXEvents() {
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Start loading effect
    document.body.addEventListener('htmx:beforeRequest', function() {
      loadingIndicator.style.transform = 'scaleX(1)';
    });

    // Finish loading effect
    document.body.addEventListener('htmx:afterSwap', function() {
      loadingIndicator.style.transform = 'scaleX(0)';
    });
  }

  // Initialize functions
  handleDropdownBehavior();
  updateActiveLink();
  handleHTMXEvents();

  // Attach htmx listener
  document.body.addEventListener('htmx:afterSwap', updateActiveLink);
  document.body.addEventListener('htmx:onLoadError', cleanLoadingIndicator);

  window.addEventListener('popstate', cleanLoadingIndicator);

});
