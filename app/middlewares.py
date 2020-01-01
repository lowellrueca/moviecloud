"""
This module contains application middlewares
"""

from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    SimpleUser, UnauthenticatedUser, AuthCredentials
from starlette.exceptions import HTTPException    
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from app.extensions import HashBuilder

REQUEST_VERIFICATION_COOKIE = 'X-Request-Verification-Token'
FORM_TOKEN_FIELD = 'antiCsrfToken'
FORWARDED_FORM_TOKEN_SESSION = 'forwarder_form_token'


class RequestVerificationCookieMiddleware(BaseHTTPMiddleware):
    """
    This class initialize request verification token for anti csrf functionality
    """

    __hash_builder__ = HashBuilder()
    __cookie_name__ = REQUEST_VERIFICATION_COOKIE

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        token = self.__hash_builder__.generate_token()
        
        # initialize cookie with token
        if self.__cookie_name__ not in request.cookies:
            response.set_cookie(self.__cookie_name__, token, max_age=60000, expires=30, path=request.base_url)

        return response


class RequestSessionVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if REQUEST_VERIFICATION_COOKIE in request.cookies and FORWARDED_FORM_TOKEN_SESSION in request.session and request.method == 'POST':
            verification_token = request.cookies[REQUEST_VERIFICATION_COOKIE]
            form_token = request.session[FORWARDED_FORM_TOKEN_SESSION]

            if form_token != verification_token:
                raise HTTPException(403, detail='Bad Request')

        return response
