"""
This module serves as a controller to handle accounts,
this also serves authenticating users for the application
"""

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, PlainTextResponse
from starlette.routing import Router, Route
from app.db import database
from app.extensions import HashBuilder
from app.middlewares import FORM_TOKEN_FIELD, SESSION_FORM_TOKEN, SESSION_ID
from app.views import template, template_env

hash_builder = HashBuilder()


async def register(request: Request):
    """
    This returns an html page for creating or registering an account
    """
    page = template_env.get_template('register.html')
    context = {'request': request}
    form = await request.form()

    if form is not None and len(form) != 0 and request.method == 'POST':
        # verify form token field and verification cookie with middleware
        request.session[SESSION_FORM_TOKEN] = form.get(FORM_TOKEN_FIELD)
        
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
    
            hash_pwd = hash_builder.generate_hash(password)
            insert = 'INSERT INTO member (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)'
            values = {'first_name': first_name,
                      'last_name': last_name,
                      'email': email,
                      'password': hash_pwd
                     }

            if fetch:
                context['email_message'] = 'Email has been registered already'
            
            elif password != confirm_password:
                context['password_message'] = 'Password not matched'
    
            else:
                await database.execute(query=insert, values=values)

    return template.TemplateResponse(page, context=context)


async def login(request: Request):
    """
    This returns an html page for logging in the users
    """
    page = template_env.get_template('login.html')
    context = {'request': request}
    session_id = hash_builder.generate_token()

    form = await request.form()
    if form is not None and len(form) != 0 and request.method == 'POST':
        email = form.get('email')
        password = form.get('password')
        hash_pwd = hash_builder.generate_hash(password)
        
        # verify form token field and verification cookie with middleware
        request.session[SESSION_FORM_TOKEN] = form.get(FORM_TOKEN_FIELD)
        
        async with database.transaction():
            query_email = 'SELECT email FROM member WHERE email = :email'
            fetch_email = await database.fetch_one(query=query_email, values={'email': email})

            query_pwd = 'SELECT password FROM member WHERE email = :email'
            fetch_pwd = await database.fetch_one(query=query_pwd, values={'email': email})

            if not fetch_email:
                context['email_message'] = 'Email has not been registered. Please Register'

            if hash_pwd != fetch_pwd['password']:
                context['password_message'] = 'Password not matched'

            else:
                insert = 'UPDATE member SET session_id = :session_id WHERE email = :email'
                values = {'session_id': session_id, 'email': email}
                await database.execute(query=insert, values=values)

                # return RedirectResponse(request.url_for('home'))
                response: Response = RedirectResponse(request.url_for('home'))
                response.set_cookie(SESSION_ID, session_id, max_age=60000, expires=30)
                return response

    return template.TemplateResponse(page, context=context)


@requires('authenticated', status_code=403)
async def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(request.url_for('login'))
    response.delete_cookie(SESSION_ID)
    return response


@requires('authenticated', redirect='login')
async def details(request: Request):
    return PlainTextResponse(f'Hello {request.user.display_name}')


routes = [
    Route('/register', endpoint=register, methods=['GET', 'POST']),
    Route('/login', endpoint=login, methods=['GET', 'POST']),
    Route('/logout', endpoint=logout, methods=['GET']),
    Route('/details', endpoint=details, methods=['GET'])
]
