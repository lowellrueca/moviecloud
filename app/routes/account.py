"""
This module serves as a controller to handle accounts,
this also serves authenticating users for the application
"""

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.routing import Router, Route
from app.db import database
from app.extensions import HashBuilder
from app.middlewares import REQUEST_VERIFICATION_COOKIE, FORM_TOKEN_FIELD, FORWARDED_FORM_TOKEN_SESSION
from app.views import template, template_env

hash_builder = HashBuilder()


async def register(request: Request):
    """
    This returns an html page for creating or registering an account
    """

    # if request.user.is_authenticated:
        # return RedirectResponse(request.url_for(''))

    page = template_env.get_template('register.html')
    context = {'request': request}
    form = await request.form()

    if form is not None and len(form) != 0 and request.method == 'POST':
        # verify form token field and verification cookie with middleware
        request.session[FORWARDED_FORM_TOKEN_SESSION] = form.get(FORM_TOKEN_FIELD)
        
        # get the values from form fields
        first_name = form.get('firstName')
        last_name = form.get('lastName')
        email = form.get('email')
        password = form.get('password')
        confirm_password = form.get('confirmPassword')

        async with database.transaction():
            # check if email has been already registered in the database
            query = 'SELECT email FROM member WHERE email = :email'
            fetch = await database.fetch_one(query=query, values={'email': email})
    
            if fetch:
                context['email_message'] = 'Email has been registered already'
            
            elif password != confirm_password:
                context['password_message'] = 'Password not matched'
    
            else:
                hash_pwd = hash_builder.generate_hash(password)
                insert = 'INSERT INTO member (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)'
                values = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': hash_pwd
                }
    
                await database.execute(query=insert, values=values)

    return template.TemplateResponse(page, context=context)


async def login(request: Request):
    """
    This returns an html page for logging in the users
    """

    page = template_env.get_template('login.html')
    context = {'request': request}

    return template.TemplateResponse(page, context=context)


account_router = Router([
    Route('/register', endpoint=register, methods=['GET', 'POST']),
    Route('/login', endpoint=login, methods=['GET', 'POST'])
])
