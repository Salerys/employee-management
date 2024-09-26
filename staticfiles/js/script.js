// Select all password fields and toggle buttons
const toggleButtons = document.querySelectorAll('.toggle-password');
const passwordFields = document.querySelectorAll('.password-field');

toggleButtons.forEach((button, index) => {
  const passwordField = passwordFields[index];
  const icon = button.querySelector('i');

  button.addEventListener('click', () => {
    const isPassword = passwordField.type === 'password';
    passwordField.type = isPassword ? 'text' : 'password';

    // Toggle the icon class between eye and eye-slash
    icon.classList.toggle('fa-eye', !isPassword);
    icon.classList.toggle('fa-eye-slash', isPassword);
  });
});

// Fade-out function for success/error messages
window.setTimeout(function () {
  const alert = document.getElementById('message-container');
  if (alert) {
    alert.style.opacity = '0';
    window.setTimeout(function () {
      alert.style.display = 'none';
    }, 1000);
  }
}, 3000);
