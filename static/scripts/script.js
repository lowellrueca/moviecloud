// initialize anti csrf token fields
let setFormTokenField = (formId, fieldName, token) => {
    form = document.getElementById(formId);
    if(form != null){
        let tokenField = document.createElement('input');
        tokenField.setAttribute('name', fieldName);
        tokenField.setAttribute('type', 'hidden');
        tokenField.setAttribute('value', token)
        form.appendChild(tokenField);
    }
}

let metaTokenField = document.getElementById('metaTokenField');
let tokenValue = metaTokenField.getAttribute('content');
let tokenFieldName = 'antiCsrfToken'
let registerForm = 'registerForm';
let loginForm = 'loginForm';

setFormTokenField(registerForm, tokenFieldName, tokenValue);
setFormTokenField(loginForm, tokenFieldName, tokenValue);

// end of script
