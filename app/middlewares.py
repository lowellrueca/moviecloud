"""
This module contains application middlewares
"""

import logging
from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    SimpleUser, UnauthenticatedUser, AuthCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        form = await request.form()
        response: Response = await call_next(request)
        print(form)
        print(type(form))
        print(request.cookies)
        print(request.session)
        return response
