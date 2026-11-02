function confirmSubmit(button) {
  const form = button.form;
  const text = form.querySelector('textarea[name="content"]').value.trim();
  if (text.length < 40) { alert('Please enter at least 40 characters.'); return false; }
  button.disabled = true; button.textContent = 'Analyzing… please wait';
  return true;
}
const contentBox = document.getElementById('content');
if (contentBox) {
  const counter = document.getElementById('counter');
  const update = () => counter.textContent = `${contentBox.value.length.toLocaleString()} / 30,000 characters`;
  contentBox.addEventListener('input', update); update();
}
