document.addEventListener("DOMContentLoaded", function() {
  function handleDropdownBehavior() {
    document.addEventListener("click", function(event) {
      const dropdown = document.getElementById("language-dropdown");
      const button = document.getElementById("language-button");
      const mobileMenu = document.getElementById("mobile-menu");
      const mobileButton = document.getElementById("mobile-menu-button");


      // Hide language dropdown if clicked outside
      if (dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target) && dropdown.style.display !== "none") {
        dropdown.style.display = "none";
      }

      // Hide mobile menu if clicked outside
      if (mobileMenu && mobileButton && !mobileMenu.contains(event.target) && !mobileButton.contains(event.target) && mobileMenu.style.display !== "none") {
        mobileMenu.style.display = "none";
      }

    });
  }

  function handleMobileMenuBehavior() {
    const mobileButton = document.getElementById("mobile-menu-button");
    const mobileMenu = document.getElementById("mobile-menu");
    const mobileLinks = mobileMenu ? mobileMenu.querySelectorAll('a') : []; // Get all anchor tags within the mobile menu

    if (mobileButton && mobileMenu) {
      mobileButton.addEventListener("click", function() {
        mobileMenu.style.display = mobileMenu.style.display === "none" ? "block" : "none";
      });
    }

    // Add this part to close the mobile menu when a link is clicked
    mobileLinks.forEach(link => {
      link.addEventListener("click", function() {
        mobileMenu.style.display = "none";
      });
    });
  }

  // Update active link in navbar
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

  // Initialize functions
  handleDropdownBehavior();
  handleMobileMenuBehavior();
  updateActiveLink();

  // Attach htmx listener
  document.body.addEventListener('htmx:afterSwap', updateActiveLink);

});
