document.addEventListener("DOMContentLoaded", function() {
  setupCopyFunctionality();
});

function setupCopyFunctionality() {
  var copyButtons = document.querySelectorAll(".copy-btn");
  copyButtons.forEach(function(button) {
      button.addEventListener("click", handleCopyClick);
  });
}

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

function getCodeFromEvent(event) {
  return event.target.parentElement.querySelector('code');
}

function copyTextToClipboard(text) {
  return navigator.clipboard.writeText(text); // This now returns a Promise
}

function displayCopyFeedback(button) {
  button.textContent = "Copied!";
  setTimeout(function() {
    button.textContent = "Copy";
  }, 800);
}

function highlightPreElement(preElement) {
  if (preElement) {
    preElement.classList.add('bg-yellow-100');

    setTimeout(function() {
      preElement.classList.remove('bg-yellow-100');
    }, 800);
  }
}
