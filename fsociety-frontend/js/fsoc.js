// Entry Point and Listener JS code goes here.

// Input
let numParaField;
let topicField;
let topicForm;

// Output
let textWell;

// Inflight
let request = null;

function getInt(n) {
  let out = parseInt(n, 10);
  if (isNaN(out) || !isFinite(out))
    out = 0;
  return out;
}

function populateOutput(text) {
  // Hide Output Panel (if currently visible from previous submission)
  if (textWell.getAttribute('hidden') === null)
    textWell.setAttribute('hidden', '');

  // Populate Output Panel
  textWell.innerHTML = '';
  textWell.appendChild(document.createTextNode(text));

  // Show Output panel
  if (text !== '')
    textWell.removeAttribute('hidden');
}

function submitSucceed(evt) {
  populateOutput(request.responseText);
  request = null;
}

function submitFail(evt) {
  let desc = request.statusText;
  if (desc === '')
    desc = 'Unknown';
  populateOutput('Error ' + request.status + ': ' + desc);
  request = null;
}

function submitStart() {
  if (request !== null)
    return;

  // Prepare input fields
  let numParas = getInt(numParaField.value);
  let topic = topicField.value;

  // Fetch Content
  let data = new FormData(topicForm);
  request = new XMLHttpRequest();
  request.addEventListener("load", submitSucceed);
  request.addEventListener("error", submitFail);
  request.addEventListener("abort", submitFail);
  request.open('POST', 'http://localhost:5000/api/v1/paragraph', true);
  request.send(data);
}

function init() {
  numParaField = document.getElementById('numParaField');
  topicField = document.getElementById('topicField');
  topicForm = document.getElementById('topicForm');
  textWell = document.getElementById('textWell');

  topicForm.addEventListener('submit', submitStart);
}

window.addEventListener('load', init, false);
