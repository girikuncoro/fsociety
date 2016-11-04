// Entry Point and Listener JS code goes here.

// Input
let numParaField;
let topicField;
let topicForm;
let srcTwitter;
let srcReddit;
let srcReuters;

// Output.
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
    populateOutput('Error parsing server response!');
    request = null;
    return;
  }

  // Assemble String.
  let outStr = '<p>';
  for (let idx = 0; idx < dataObj.data.length; ++idx) {
    if (idx !== 0)
      outStr += '</p><p>';
    outStr += escapeHTML(dataObj.data[idx]);
  }
  outStr += '</p>';

  // Display.
  populateOutput(outStr);
  request = null;
}

function submitFail(evt) {
  let desc = request.statusText;
  if (desc === '')
    desc = 'Failed to Connect to Backend';
  populateOutput('Error ' + request.status + ': ' + desc);
  request = null;
}

function submitStart() {
  // Don't make a request if one is already in progress.
  if (request !== null)
    return;

  // Prepare input.
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
  request.open('POST', 'http://localhost:5000/api/v1/paragraph/' + suffix, true);
  request.send(data);
}

function init() {
  // Get references to the important elements.
  numParaField = document.getElementById('numParaField');
  topicField = document.getElementById('topicField');
  topicForm = document.getElementById('topicForm');
  textWell = document.getElementById('textWell');
  srcTwitter = document.getElementById('srcTwitter');
  srcReddit = document.getElementById('srcReddit');
  srcReuters = document.getElementById('srcReuters');

  // Set submit listener.
  topicForm.addEventListener('submit', submitStart);
}

// Run the initializer once the document is ready. No sooner.
window.addEventListener('load', init, false);
