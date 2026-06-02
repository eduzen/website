document.addEventListener("DOMContentLoaded", function() {
  function normalizePathname(path) {
    if (!path) return "";

    try {
      return new URL(path, window.location.origin).pathname;
    } catch (err) {
      console.debug("Unable to normalize navigation path", err);
      return path;
    }
  }

  function storageKey(pathname) {
    return "view:" + normalizePathname(pathname);
  }

  function setStoredView(pathname, currentView) {
    if (!pathname || !currentView) return;

    try {
      sessionStorage.setItem(storageKey(pathname), currentView);
    } catch (err) {
      console.debug("Unable to store current navigation view", err);
    }
  }

  function getStoredView(pathname) {
    try {
      return sessionStorage.getItem(storageKey(pathname));
    } catch (err) {
      console.debug("Unable to read current navigation view", err);
      return null;
    }
  }

  function updateActiveNavigation(currentView, pathname) {
    var nav = document.getElementById("main-navbar");
    if (!nav) return;

    if (!currentView) {
      currentView = nav.dataset.currentView || "";
    }
    nav.dataset.currentView = currentView;
    setStoredView(pathname || window.location.pathname, currentView);

    nav.querySelectorAll(".active-link").forEach(function(el) {
      el.classList.remove("active-link");
    });
    nav.querySelectorAll(".nav-dropdown__item--active").forEach(function(el) {
      el.classList.remove("nav-dropdown__item--active");
    });

    var selectors = [
      ".logo[data-nav-sections]",
      ".nav-link[data-nav-sections]",
      ".nav-dropdown__trigger[data-nav-sections]",
      ".nav-dropdown__item[data-nav-sections]"
    ].join(", ");

    nav.querySelectorAll(selectors).forEach(function(item) {
      var sections = (item.dataset.navSections || "").split(/\s+/).filter(Boolean);
      if (sections.includes(currentView)) {
        if (item.classList.contains("nav-dropdown__item")) {
          item.classList.add("nav-dropdown__item--active");
        } else {
          item.classList.add("active-link");
        }
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

    document.body.addEventListener("htmx:afterSettle", function(evt) {
      var xhr = evt.detail.xhr;
      var view = xhr && xhr.getResponseHeader ? xhr.getResponseHeader("X-Current-View") : null;
      updateActiveNavigation(view);
    });

    document.body.addEventListener("htmx:pushedIntoHistory", function(evt) {
      updateActiveNavigation(null, evt.detail.path);
    });

    document.body.addEventListener("htmx:replacedInHistory", function(evt) {
      updateActiveNavigation(null, evt.detail.path);
    });
  }

  handleHTMXEvents();
  updateActiveNavigation();

  window.addEventListener("popstate", function() {
    var view = getStoredView(window.location.pathname);
    updateActiveNavigation(view);
  });
});
