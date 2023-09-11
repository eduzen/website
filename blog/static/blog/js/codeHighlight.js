// Initialize the setupCopyFunctionality function upon page content loading
document.addEventListener("DOMContentLoaded", function() {
  setupCopyFunctionality();
});

// Listen for htmx's afterSwap event to reinitialize the copy functionality for newly loaded content
document.body.addEventListener('htmx:afterSwap', function() {
  setupCopyFunctionality();
});

// This function initializes copy buttons' functionality
function setupCopyFunctionality() {
  var copyButtons = document.querySelectorAll(".copy-btn");
  copyButtons.forEach(function(button) {
      button.addEventListener("click", handleCopyClick);
  });
}

// This function handles the click event for copy buttons
function handleCopyClick(event) {
  var code = getCodeFromEvent(event);
  if (!code) {
    console.warn("No <code> tag found within this <pre> tag.");
    return;
  }

  copyTextToClipboard(code.textContent)
    .then(function() {
      displayCopyFeedback(event.target);
      highlightPreElement(event.target.parentElement);
    })
    .catch(function(err) {
      console.warn("Failed to copy text", err);
    });
}

// Extracts the <code> tag from the clicked copy button's event
function getCodeFromEvent(event) {
  return event.target.parentElement.querySelector('code');
}

// Uses the Clipboard API to copy the provided text to the clipboard
function copyTextToClipboard(text) {
  return navigator.clipboard.writeText(text); // This now returns a Promise
}

// Shows feedback upon successful copy action
function displayCopyFeedback(button) {
  button.textContent = "Copied!";
  setTimeout(function() {
    button.textContent = "Copy";
  }, 800);
}

// Temporarily highlights the <pre> element to visually indicate a copy action
function highlightPreElement(preElement) {
  if (preElement) {
    preElement.classList.add('bg-yellow-100');

    setTimeout(function() {
      preElement.classList.remove('bg-yellow-100');
    }, 800);
  }
}
