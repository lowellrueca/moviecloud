// anti csrf implementation script
let antiCSRFField = document.getElementById('anti-csrf-field');
let tokenValue = antiCSRFField.getAttribute('content');
let loginForm = document.getElementById('login-form');

if (loginForm != null) {
    let csrfField = document.createElement('input');
    csrfField.setAttribute('name', 'anti-csrf-field');
    csrfField.setAttribute('type', 'hidden');
    csrfField.setAttribute('value', tokenValue)
    loginForm.appendChild(csrfField);
}
