// Inject copy buttons into <pre> blocks inside .post-content.
// This file is part of the post-detail partial, so it re-runs on every HTMX navigation to a post:
// listeners are bound once, and processed blocks are marked to stay idempotent.

function initCopyButtons() {
  document.querySelectorAll(".post-content pre:not([data-copy-btn])").forEach(function (pre) {
    pre.dataset.copyBtn = "true";

    var codeEl = pre.querySelector("code");
    if (codeEl) {
      // Remove stray "Copy" text nodes that were copy-pasted into the content
      var node = codeEl.nextSibling;
      while (node) {
        var next = node.nextSibling;
        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().toLowerCase() === "copy") {
          node.remove();
        }
        node = next;
      }

      if (typeof hljs !== "undefined") {
        hljs.highlightElement(codeEl);
      }
    }

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-code-btn";
    btn.setAttribute("aria-label", "Copy code to clipboard");
    btn.textContent = "Copy";

    btn.addEventListener("click", function () {
      var text = (codeEl || pre).textContent;
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "Copied!";
        btn.classList.add("copied");
        setTimeout(function () {
          btn.textContent = "Copy";
          btn.classList.remove("copied");
        }, 1500);
      }).catch(function (err) {
        console.warn("Failed to copy code", err);
      });
    });

    pre.appendChild(btn);
  });
}

if (!window.copyCodeListenerBound) {
  window.copyCodeListenerBound = true;
  document.body.addEventListener("htmx:afterSwap", initCopyButtons);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initCopyButtons);
} else {
  initCopyButtons();
}
