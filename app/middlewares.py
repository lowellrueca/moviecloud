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

SESSION_ID = 'X-Session-Id'


class AntiCsrfMiddleware(BaseHTTPMiddleware):
    """
    This class initialize request verification token and validates posted token.

    """

    __hash_builder__ = HashBuilder()
    __cookie__ = 'X-Request-Verification-Token'
    __session__ = 'request_verification_session'
    __token_field__ = 'anti-csrf-token'

    async def init_cookie(self, request: Request, response: Response):
        """
        Initilizes cookie and sends the request verification token to the client
        """
        token = self.__hash_builder__.generate_token()
        if self.__cookie__ not in request.cookies:
            response.set_cookie(self.__cookie__, token, max_age=60000, expires=30, path=request.base_url)

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        await self.init_cookie(request, response)

        if self.__cookie__ in request.cookies \
            and self.__session__ in request.session \
            and request.method == 'POST':

            cookie_token = request.cookies[self.__cookie__]
            session_token = request.session[self.__session__]
            if session_token != cookie_token:
                page = template_env.get_template('error_403.html')
                context = {'request': request}
                return template.TemplateResponse(page, context=context, status_code=403)

        return response

    @classmethod
    async def validate_anti_csrf_token(cls, request: Request, form: FormData):
        """
        This method sets the session which holds the token with the post request from form's hidden input field,
        and validates within this class dispatch method.

        Usage:
        async def endpoint(request):
            form = await request.form()
            if len(form) != 0 and request.method is == 'POST:
                await AtniCsrfMiddleware.validate_anti_csrf_token(request, form)

        Parameters:
        request -> The request object
        form    -> The form data object
        """
        request.session[AntiCsrfMiddleware.__session__] = form.get(AntiCsrfMiddleware.__token_field__)


class AuthenticateMemberMiddleware(AuthenticationBackend):
    __session_id__ = SESSION_ID

    async def authenticate(self, request: Request):
        if self.__session_id__ not in request.cookies: return

        session_id = request.cookies[self.__session_id__]
        async with database.transaction():
            query = 'SELECT first_name, role FROM member WHERE session_id = :session_id'
            fetch = await database.fetch_one(query=query, values={'session_id': session_id})
            
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
