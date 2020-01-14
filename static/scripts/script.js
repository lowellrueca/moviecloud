// window.onload = () => {
//     initializeAntiCsrfFormTokens();
// }

// let initializeAntiCsrfFormTokens = () => {
//     let appendAntiCsrfToken = (formId, tokenValue) => {
//         let name = 'anti-csrf-token';
//         let form = document.getElementById(formId);
//         if(form != null){
//             let antiCsrfField = document.createElement('input');
//             antiCsrfField.setAttribute('name', name);
//             antiCsrfField.setAttribute('type', 'hidden');
//             antiCsrfField.setAttribute('value', tokenValue);
//             form.appendChild(antiCsrfField);
//         }
//     }

//     let metaTokenField = document.getElementById('meta-token');
//     let metaTokenValue = metaTokenField.getAttribute('content');
//     let registerForm = 'register-form';
//     let loginForm = 'login-form';
//     appendAntiCsrfToken(registerForm, metaTokenValue);
//     appendAntiCsrfToken(loginForm, metaTokenValue);
// }
