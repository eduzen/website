document.addEventListener("DOMContentLoaded", function() {
  function getCurrentSection(pathname) {
    var path = pathname.replace(/^\/+|\/+$/g, "");
    if (!path) return "home";

    var segments = path.split("/");
    if (segments[0] === "en" || segments[0] === "es") {
      segments.shift();
    }

    return segments[0] || "home";
  }

  function isNavItemActive(item, currentPath, currentSection) {
    var sections = (item.dataset.navSections || "")
      .split(/\s+/)
      .map(function(section) { return section.trim(); })
      .filter(Boolean);

    if (sections.length > 0) {
      return sections.includes(currentSection);
    }

    if (item.tagName !== "A") return false;

    var href = item.getAttribute("href");
    if (!href || href.startsWith("#") || href.startsWith("?")) return false;

    var hrefPath = new URL(href, window.location.origin).pathname.replace(/\/+$/, "") || "/";
    return currentPath === hrefPath || (hrefPath !== "/" && currentPath.startsWith(hrefPath + "/"));
  }

  function updateActiveNavigation() {
    var nav = document.getElementById("main-navbar");
    if (!nav) return;

    var currentPath = window.location.pathname.replace(/\/+$/, "") || "/";
    var currentSection = getCurrentSection(window.location.pathname);
    var navItems = nav.querySelectorAll(".logo, .nav-link, .nav-dropdown__trigger");

    navItems.forEach(function(item) {
      item.classList.remove("active-link");
      if (isNavItemActive(item, currentPath, currentSection)) {
        item.classList.add("active-link");
      }
    });

    var dropdownItems = nav.querySelectorAll(".nav-dropdown__item[data-nav-sections]");
    dropdownItems.forEach(function(item) {
      item.classList.remove("nav-dropdown__item--active");
      if (isNavItemActive(item, currentPath, currentSection)) {
        item.classList.add("nav-dropdown__item--active");
      }
    });
  }
  function handleHTMXEvents() {
    var indicator = document.getElementById("loadingIndicator");

    document.body.addEventListener("htmx:beforeRequest", function() {
      if (indicator) {
        indicator.classList.remove("scale-x-0");
        indicator.classList.add("scale-x-100");
      }
    });

    document.body.addEventListener("htmx:afterRequest", function() {
      if (indicator) {
        setTimeout(function() {
          indicator.classList.remove("scale-x-100");
          indicator.classList.add("scale-x-0");
        }, 200);
      }
    });

    document.body.addEventListener("htmx:responseError", function(evt) {
      console.error("HTMX Request failed:", evt.detail);
      if (indicator) {
        indicator.classList.remove("scale-x-100");
        indicator.classList.add("scale-x-0");
        indicator.style.background = "var(--error)";
        setTimeout(function() {
          indicator.style.background = "";
        }, 2000);
      }
    });

    document.body.addEventListener("htmx:afterSettle", function() {
      if (window.location.pathname !== lastPath) {
        lastPath = window.location.pathname;
      }
      updateActiveNavigation();
    });
  }

  var lastPath = window.location.pathname;

  handleHTMXEvents();
  updateActiveNavigation();

  window.addEventListener("popstate", function() {
    lastPath = window.location.pathname;
    updateActiveNavigation();
  });
});
