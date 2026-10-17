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

    nav.querySelectorAll("[data-nav-sections]").forEach(function(item) {
      var sections = item.dataset.navSections.split(/\s+/).filter(Boolean);
      var activeClass = item.classList.contains("nav-dropdown__item") ? "nav-dropdown__item--active" : "active-link";
      item.classList.toggle(activeClass, sections.includes(currentView));
    });
  }

  function handleHTMXEvents() {
    var indicator = document.getElementById("loadingIndicator");

    function showIndicator(visible) {
      if (!indicator) return;
      indicator.classList.toggle("scale-x-100", visible);
      indicator.classList.toggle("scale-x-0", !visible);
    }

    document.body.addEventListener("htmx:beforeRequest", function() {
      showIndicator(true);
    });

    document.body.addEventListener("htmx:afterRequest", function() {
      setTimeout(showIndicator, 200, false);
    });

    document.body.addEventListener("htmx:responseError", function(evt) {
      console.error("HTMX Request failed:", evt.detail);
      showIndicator(false);
      if (indicator) {
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

    function onHistoryUpdate(evt) {
      updateActiveNavigation(null, evt.detail.path);
    }
    document.body.addEventListener("htmx:pushedIntoHistory", onHistoryUpdate);
    document.body.addEventListener("htmx:replacedInHistory", onHistoryUpdate);
  }

  handleHTMXEvents();
  updateActiveNavigation();

  window.addEventListener("popstate", function() {
    var view = getStoredView(window.location.pathname);
    updateActiveNavigation(view);
  });
});
