// Inject copy buttons into <pre> blocks inside .post-content
// Re-initializes on HTMX swaps so it works with partial page loads.

document.addEventListener("DOMContentLoaded", initCopyButtons);
document.body.addEventListener("htmx:afterSwap", initCopyButtons);

function initCopyButtons() {
  var blocks = document.querySelectorAll(".post-content pre");
  blocks.forEach(function (pre) {
    // Skip if already processed
    if (pre.dataset.copyBtn === "true") return;
    pre.dataset.copyBtn = "true";

    // Ensure the <pre> is positioned for absolute child placement
    var style = window.getComputedStyle(pre);
    if (style.position === "static") {
      pre.style.position = "relative";
    }

    // Remove stray "Copy" text nodes that were copy-pasted into the content
    var codeEl = pre.querySelector("code");
    if (codeEl) {
      var next = codeEl.nextSibling;
      while (next) {
        var toRemove = next;
        next = next.nextSibling;
        if (toRemove.nodeType === Node.TEXT_NODE && toRemove.textContent.trim().toLowerCase() === "copy") {
          toRemove.remove();
        }
      }

      // Syntax highlight
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
      var code = pre.querySelector("code");
      var text = code ? code.textContent : pre.textContent;

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
