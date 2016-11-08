// Entry Point and Listener JS code goes here.

// Input
let numParaField;
let topicField;
let topicForm;
let srcTwitter;
let srcReddit;
let srcReuters;
let submitBtn;

// Output.
let errToggle;
let errWell;
let textWell;

// Inflight.
let request = null;

// To aid the escape function.
let ESC_MAP = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
  '/': '&#47;'
};

// Basic HTML escape.
function escapeHTML(s) {
  // We can escape the string in 1 pass with the right regex and function.
  return s.replace(/[&<>'"\/]/g, function(c) {
    return ESC_MAP[c];
  });
}

function populateOutput(text) {
  // Hide Output Panel (if currently visible from previous submission).
  if (textWell.getAttribute('hidden') === null)
    textWell.setAttribute('hidden', '');

  // Populate Output Panel.
  textWell.innerHTML = text;

  // Show Output panel.
  if (text !== '')
    textWell.removeAttribute('hidden');
}

function populateError(text) {
  // Hide Error Panel (if currently visible from previous submission).
  if (errToggle.getAttribute('hidden') === null)
    errToggle.setAttribute('hidden', '');

  // Populate Error Panel.
  errWell.innerHTML = text;

  // Show Error panel.
  if (text !== '')
    errToggle.removeAttribute('hidden');
}

function submitSucceed(evt) {
  // Parse or Abort.
  if (request.status >= 400) {
    submitFail();
    return;
  }
  let dataObj;
  try {
    dataObj = JSON.parse(request.responseText);
  } catch (ex) {
    populateError('Error parsing server response!');
    submitCleanup();
    return;
  }

  // Assemble String.
  let outStr = '<p>';
  if (dataObj.data.length !== 0) {
    for (let idx = 0; idx < dataObj.data.length; ++idx) {
      if (idx !== 0)
        outStr += '</p><p>';
      outStr += escapeHTML(dataObj.data[idx]);
    }
  } else {
    outStr += 'No Data on this Topic';
  }
  outStr += '</p>';

  // Display.
  populateError('');
  populateOutput(outStr);
  submitCleanup();
}

function submitFail(evt) {
  let desc = request.statusText;
  if (desc === '')
    desc = 'Failed to Connect to Backend';
  populateError('<strong>Error&nbsp;' + request.status + ':</strong> ' + desc);
  submitCleanup();
}

function submitCleanup() {
  // Re-enable input fields.
  request = null;
  numParaField.readOnly = false;
  topicField.readOnly = false;
  srcTwitter.disabled = false;
  srcReddit.disabled = false;
  srcReuters.disabled = false;
  submitBtn.disabled = false;
  submitBtn.className = 'btn btn-primary';
  submitBtn.innerHTML = 'Get Filler';
}

function submitStart() {
  // Don't make a request if one is already in progress.
  if (request !== null)
    return;

  // Prepare input.
  numParaField.readOnly = true;
  topicField.readOnly = true;
  srcTwitter.disabled = true;
  srcReddit.disabled = true;
  srcReuters.disabled = true;
  submitBtn.disabled = true;
  submitBtn.className = 'btn btn-info';
  submitBtn.innerHTML = 'Fetching...';
  let suffix;
  if (srcReuters.checked) {
    suffix = 'reuters';
  } else if (srcReddit.checked) {
    suffix = 'reddit';
  } else {
    suffix = 'twitter';
  }

  // Fetch Content.
  let data = new FormData(topicForm);
  request = new XMLHttpRequest();
  request.addEventListener("load", submitSucceed);
  request.addEventListener("error", submitFail);
  request.addEventListener("abort", submitFail);
  request.open('POST', '/api/v1/paragraph/' + suffix, true);
  request.send(data);
}

function init() {
  // Get references to the important elements.
  numParaField = document.getElementById('numParaField');
  topicField = document.getElementById('topicField');
  topicForm = document.getElementById('topicForm');
  srcTwitter = document.getElementById('srcTwitter');
  srcReddit = document.getElementById('srcReddit');
  srcReuters = document.getElementById('srcReuters');
  submitBtn = document.getElementById('submitBtn');
  errToggle = document.getElementById('errToggle');
  errWell = document.getElementById('errWell');
  textWell = document.getElementById('textWell');

  // Set submit listener.
  topicForm.addEventListener('submit', submitStart);
}

// Run the initializer once the document is ready. No sooner.
window.addEventListener('load', init, false);
