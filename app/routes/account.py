"""
This module serves as a controller to handle accounts,
this also serves authenticating users for the application
"""

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, PlainTextResponse, HTMLResponse
from starlette.routing import Router, Route
from app.db import database
from app.extensions import HashBuilder
from app.middlewares import AntiCsrfMiddleware, AuthenticateMemberMiddleware
from app.resources import template, template_env

hash_builder = HashBuilder()


async def register(request: Request):
    """
    This returns an html page for creating or registering an account
    """
    page = template_env.get_template('register.html')
    context = {'request': request}
    form = await request.form()

    if form is not None and len(form) != 0 and request.method == 'POST':
        await AntiCsrfMiddleware.validate_anti_csrf_token(request, form)

        # get the values from form fields
        first_name = form.get('firstName')
        last_name = form.get('lastName')
        email = form.get('email')
        password = form.get('password')
        confirm_password = form.get('confirmPassword')

        async with database.transaction():
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
                return PlainTextResponse('Email has been registered already')
            
            elif password != confirm_password:
                return PlainTextResponse('Password not matched')
    
            else:
                await database.execute(query=insert, values=values)
                html = f"<span>You've been sucessfully registered {first_name}, you may now <a href={request.url_for('login')}>Login</a></span>"
                return HTMLResponse(html)

    return template.TemplateResponse(page, context=context)


async def login(request: Request):
    """
    This returns an html page for logging in the users
    """
    page = template_env.get_template('login.html')
    context = {'request': request}
    await AntiCsrfMiddleware.send_cookie_token(request, context)

    form = await request.form()
    if form is not None and len(form) != 0 and request.method == 'POST':
        email = form.get('email')
        password = form.get('password')
        hash_pwd = hash_builder.generate_hash(password)

        async with database.transaction():
            query_email = 'SELECT email FROM member WHERE email = :email'
            fetch_email = await database.fetch_one(query=query_email, values={'email': email})

            query_pwd = 'SELECT password FROM member WHERE email = :email'
            fetch_pwd = await database.fetch_one(query=query_pwd, values={'email': email})

            if not fetch_email:
                return PlainTextResponse('Email has not been registered. Please Register', status_code=401)

            if hash_pwd != fetch_pwd['password']:
                return PlainTextResponse('Password not matched', status_code=401)

            else:
                auth_key = AuthenticateMemberMiddleware.auth_key
                auth_token = hash_builder.generate_token()

                update = 'UPDATE member SET auth_id = :auth_id WHERE email = :email'
                values = {auth_key: auth_token, 'email': email}
                await database.execute(query=update, values=values)

                # initialize the session to verify user authentication with AuthenticationMemberMIddleware
                request.session[auth_key] = auth_token

                # # return redirect response and delete anti csrf cookie to reset with AntiCsrfMiddleware
                response: Response = RedirectResponse(request.url_for('home'))
                response.delete_cookie(AntiCsrfMiddleware.anti_csrf_cookie)
                return response

    return template.TemplateResponse(page, context=context)


@requires('authenticated', status_code=403)
async def logout(request: Request):
    request.session.pop(AuthenticateMemberMiddleware.auth_key, None)
    response = RedirectResponse(request.url_for('login'))
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
