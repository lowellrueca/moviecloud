"""
This module contains application middlewares
"""

import logging
from starlette.requests import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    SimpleUser, UnauthenticatedUser, AuthCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from app.views import template, template_env


class AntiCSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        
        form = await request.form()
        if len(form) != 0 and 'Request-Verification-Token' in request.cookies:
            anti_csrf_field = form.get('anti-csrf-field')
            verification_token = request.cookies['Request-Verification-Token']
            
            if anti_csrf_field != verification_token:
                page = template_env.get_template('error_403.html')
                context = {'request': request}
                return template.TemplateResponse(page, context=context)

        return response
