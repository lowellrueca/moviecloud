// initialize anti csrf token fields
let setFormTokenField = (formId, fieldName, tokenValue) => {
    form = document.getElementById(formId);
    if(form != null){
        let tokenField = document.createElement('input');
        tokenField.setAttribute('name', fieldName);
        tokenField.setAttribute('type', 'hidden');
        tokenField.setAttribute('value', tokenValue)
        form.appendChild(tokenField);
    }
}

let metaTokenField = document.getElementById('metaTokenField');
let metaTokenValue = metaTokenField.getAttribute('content');
let formTokenField = 'formToken'
let registerFormId = 'registerForm';
let loginFormId = 'loginForm';

setFormTokenField(registerFormId, formTokenField, metaTokenValue);
setFormTokenField(loginFormId, formTokenField, metaTokenValue);

// end of script
