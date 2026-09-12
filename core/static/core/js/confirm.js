// Custom confirmation dialog — replaces native browser confirm()
// Works with any form that has a data-confirm attribute.
// Shows a preview of the form data before sending.
(function () {
  var dialog = document.getElementById('confirmDialog');
  if (!dialog) return;

  var previewEl = document.getElementById('confirmPreview');
  var pendingForm = null;

  // Build a preview of the form's visible fields
  function buildPreview(form) {
    if (!previewEl) return;
    previewEl.innerHTML = '';

    var fields = form.querySelectorAll('input[type="text"], input[type="email"], textarea');
    fields.forEach(function (field) {
      var value = field.value.trim();
      if (!value) return;

      // Skip captcha / hidden / utility fields
      if (field.name === 'captcha' || field.name === 'csrfmiddlewaretoken') return;

      // Find the label text
      var label = '';
      var labelEl = form.querySelector('label[for="' + field.id + '"]');
      if (labelEl) {
        label = labelEl.textContent.replace(/\*$/, '').trim();
      }
      if (!label) label = field.name;

      var row = document.createElement('div');
      row.className = 'confirm-dialog__field';

      var labelSpan = document.createElement('span');
      labelSpan.className = 'confirm-dialog__field-label';
      labelSpan.textContent = label;

      var valueSpan = document.createElement('span');
      valueSpan.className = 'confirm-dialog__field-value';

      // Truncate long messages
      if (field.tagName === 'TEXTAREA' && value.length > 120) {
        valueSpan.textContent = value.substring(0, 120) + '…';
      } else {
        valueSpan.textContent = value;
      }

      row.appendChild(labelSpan);
      row.appendChild(valueSpan);
      previewEl.appendChild(row);
    });
  }

  // Update the dialog title and confirm button from data attributes
  function configure(form) {
    var titleEl = dialog.querySelector('.confirm-dialog__title');
    if (titleEl && form.dataset.confirmTitle) {
      titleEl.textContent = form.dataset.confirmTitle;
    }

    var okLabel = form.dataset.confirmOk || 'Send';
    var okBtn = dialog.querySelector('.confirm-dialog__btn--confirm');
    if (okBtn) okBtn.textContent = okLabel;
  }

  // Intercept submit on forms with data-confirm
  document.addEventListener('submit', function (evt) {
    var form = evt.target;
    if (!form.dataset.confirm || form.dataset.confirmBypassed) return;

    evt.preventDefault();
    evt.stopPropagation();
    pendingForm = form;
    configure(form);
    buildPreview(form);
    dialog.showModal();
  }, true); // Use capture phase to run before HTMX

  // Handle dialog close
  dialog.addEventListener('close', function () {
    if (!pendingForm) return;

    if (dialog.returnValue === 'confirm') {
      // Temporarily bypass the confirm to allow resubmission
      pendingForm.dataset.confirmBypassed = 'true';
      pendingForm.requestSubmit();

      // Clean up after HTMX picks up the submission
      requestAnimationFrame(function () {
        if (pendingForm) delete pendingForm.dataset.confirmBypassed;
        pendingForm = null;
      });
    } else {
      pendingForm = null;
    }
  });

  // Close on click outside the dialog box
  dialog.addEventListener('click', function (evt) {
    if (evt.target === dialog) dialog.close('cancel');
  });
})();
