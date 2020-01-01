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

FORM_TOKEN_FIELD = 'formToken'
SESSION_FORM_TOKEN = 'session_form_token'
REQUEST_VERIFICATION_COOKIE = 'X-Request-Verification-Token'


class AntiCsrfMiddleware(BaseHTTPMiddleware):
    """
    This class initialize request verification token for anti csrf functionality
    """

    __hash_builder__ = HashBuilder()
    __cookie_name__ = REQUEST_VERIFICATION_COOKIE
    __session_form_token__ = SESSION_FORM_TOKEN

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        token = self.__hash_builder__.generate_token()
        
        # initialize cookie with token
        if self.__cookie_name__ not in request.cookies:
            response.set_cookie(self.__cookie_name__, token, max_age=60000, expires=30, path=request.base_url)

        if self.__cookie_name__ in request.cookies \
            and self.__session_form_token__ in request.session \
            and request.method == 'POST':

            verification_token = request.cookies[REQUEST_VERIFICATION_COOKIE]
            form_token = request.session[SESSION_FORM_TOKEN]

            if form_token != verification_token:
                raise HTTPException(403, detail='Bad Request')

        return response
