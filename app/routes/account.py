"""
This module serves as a controller to handle accounts,
this also serves authenticating users for the application
"""

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Router, Route
from app.views import template, template_env
from app.extensions import HashBuilder

hasher = HashBuilder()


async def register(request: Request):
    """
    This returns an html page for creating or registering an account
    """

    page = template_env.get_template('register.html')
    context = {'request': request}
    return template.TemplateResponse(page, context=context)


async def login(request: Request):
    """
    This returns an html page for logging in the users
    """

    page = template_env.get_template('login.html')
    context = {'request': request}
    token = hasher.generate_token()
    request.session['anti-csrf-token'] = token
    
    response: Response = template.TemplateResponse(page, context=context)
    response.set_cookie('Request-Verification-Token', token, max_age=60000, expires=30, httponly=True)
    return response


account_router = Router([
    Route('/register', endpoint=register, methods=['GET', 'POST']),
    Route('/login', endpoint=login, methods=['GET', 'POST'])
])
