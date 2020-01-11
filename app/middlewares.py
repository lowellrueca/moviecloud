"""
This module contains application middlewares
"""

from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    SimpleUser, UnauthenticatedUser, AuthCredentials
from starlette.datastructures import FormData
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from app.db import database
from app.extensions import HashBuilder
from app.resources import template, template_env


class AntiCsrfMiddleware(BaseHTTPMiddleware):
    """
    This class initialize request verification token and validates posted token.

    """

    __hash_builder__ = HashBuilder()
    anti_csrf_cookie = 'X-Request-Verification-Token'
    anti_csrf_session = 'request_verification_session'
    anti_csrf_field = 'anti-csrf-token'

    async def init_cookie(self, request: Request, response: Response):
        """
        Initilizes cookie and sends the request verification token to the client
        """
        token = self.__hash_builder__.generate_token()
        if self.anti_csrf_cookie not in request.cookies:
            response.set_cookie(self.anti_csrf_cookie, token, max_age=60000, expires=30, path=request.base_url)

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        await self.init_cookie(request, response)

        if self.anti_csrf_cookie in request.cookies \
            and self.anti_csrf_session in request.session \
            and request.method == 'POST':

            cookie_token = request.cookies[self.anti_csrf_cookie]
            session_token = request.session[self.anti_csrf_session]
            if session_token != cookie_token:
                page = template_env.get_template('error_403.html')
                context = {'request': request}
                return template.TemplateResponse(page, context=context, status_code=403)

        return response

    @staticmethod
    async def validate_anti_csrf_token(request: Request, form: FormData):
        """
        This method sets the session which holds the token with the post request from form's hidden input field,
        and validates within this class dispatch method.

        Usage:
        async def endpoint(request):
            form = await request.form()
            if len(form) != 0 and request.method is == 'POST:
                await AntiCsrfMiddleware.validate_anti_csrf_token(request, form)

        Parameters:
        request -> The request object
        form    -> The form data object
        """
        request.session[AntiCsrfMiddleware.anti_csrf_session] = form.get(AntiCsrfMiddleware.anti_csrf_field)


class AuthenticateMemberMiddleware(AuthenticationBackend):
    __hash_builder__ = HashBuilder()
    auth_key = 'auth_id'
    
    async def authenticate(self, request: Request):
        if self.auth_key not in request.cookies: return

        auth_id = request.cookies[self.auth_key]
        async with database.transaction():
            query = 'SELECT first_name, role FROM member WHERE auth_id = :auth_id'
            fetch = await database.fetch_one(query=query, values={'auth_id': auth_id})
            
            if fetch:
                first_name = fetch['first_name']
                role = fetch['role']

                if role != 'admin':
                    return AuthCredentials(['authenticated']), SimpleUser(first_name)

                elif role == 'admin':
                    return AuthCredentials(['authenticated', 'admin']), SimpleUser(first_name)
            
            else:
                return None


class PreventPublicAuthMiddleware(BaseHTTPMiddleware):
    """
    This class returns redirect response to member's account details,
    preventing the member to access login and register routes if they
    have been successfully authenticated.
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        register_url = f'{request.base_url}account/register'
        login_url = f'{request.base_url}account/login'

        if request.url == register_url or request.url == login_url:
            if request.user.is_authenticated:
                return RedirectResponse(request.url_for('details'))

        return response
