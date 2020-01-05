"""
This module serves to initialize the application factory
"""

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Mount

# import application middlewares
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from app.middlewares import AntiCsrfMiddleware, AuthenticateMemberMiddleware
from app.middlewares import PreventPublicAuthMiddleware

# import static file class
from starlette.staticfiles import StaticFiles

# import app configurations
from app.config import DEBUG, STATIC_ROOT, SECRET_KEY

# import event handlers
from app.events import startup, shutdown

# import routes and exception handlers
from app.routes import index, account
from app.routes.exceptions import error_403, error_404, error_500


def init_app():
    routes = [
        Mount('/static', StaticFiles(directory=STATIC_ROOT), name='static'),
        Mount('/account', routes=account.routes),
        Mount('/', routes=index.routes)
    ]

    middlewares = [
        Middleware(AntiCsrfMiddleware),
        Middleware(AuthenticationMiddleware, backend=AuthenticateMemberMiddleware()),
        Middleware(PreventPublicAuthMiddleware),
        Middleware(SessionMiddleware, secret_key=SECRET_KEY)
    ]

    exception_handlers = {
        403: error_403,
        404: error_404,
        405: error_500
    }

    app = Starlette(
        debug=DEBUG, 
        routes=routes, 
        middleware=middlewares, 
        exception_handlers=exception_handlers,
        on_startup=[startup],
        on_shutdown=[shutdown]
    )

    return app
