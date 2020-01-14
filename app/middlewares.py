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
from starlette.responses import Response, RedirectResponse, PlainTextResponse
from app.db import database
from app.extensions import HashBuilder
from app.resources import template, template_env


class AntiCsrfMiddleware(BaseHTTPMiddleware):
    """
    This class initialize request verification token and validates posted token.

    """

    __hash_builder__ = HashBuilder()
    anti_csrf_cookie = 'X-CSRF-Token'

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

        if self.anti_csrf_cookie in request.cookies and request.method == 'POST':
            cookie_token = request.cookies[self.anti_csrf_cookie]
            x_csrf_token = request.headers.get(self.anti_csrf_cookie.lower())

            if x_csrf_token != cookie_token:
                return Response(status_code=400)

        return response

    @staticmethod
    async def send_cookie_token(request: Request, context: dict):
        if AntiCsrfMiddleware.anti_csrf_cookie in request.cookies:
            cookie_token = request.cookies[AntiCsrfMiddleware.anti_csrf_cookie]
            context['x_csrf_key'] = AntiCsrfMiddleware.anti_csrf_cookie.lower()
            context['x_csrf_token'] = cookie_token


class AuthenticateMemberMiddleware(AuthenticationBackend):
    __hash_builder__ = HashBuilder()
    auth_key = 'auth_id'
    
    async def authenticate(self, request: Request):
        # validate x-csrf-token header with cookie token
        if AntiCsrfMiddleware.anti_csrf_cookie in request.cookies \
            and 'x-csrf-token' in request.headers:

            cookie_token = request.cookies[AntiCsrfMiddleware.anti_csrf_cookie]
            x_csrf_header = {k: v for k, v in request.headers.items() if k == AntiCsrfMiddleware.anti_csrf_cookie.lower()}
            for x_csrf_key, x_csrf_token in x_csrf_header.items():
                if x_csrf_token != cookie_token:
                    raise AuthenticationError('Failed to send request due with tokens not matched')
        
        # return if auth_id not in request session
        if self.auth_key not in request.session: return

        # proceed to fetch user/ member
        auth_id = request.session[self.auth_key]
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
