"""
This module serves to initialize the application factory
"""

from starlette.applications import Starlette as App

# import application middlewares
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from app.middlewares import AntiCsrfMiddleware, AuthenticateMemberMiddleware
from app.middlewares import PreventPublicAuthMiddleware

# import static file class
from starlette.staticfiles import StaticFiles

# import app configurations
from app.config import DEBUG, SECRET_KEY

# import resources
from app.resources import STATIC_PATH

# import event handlers
from app.events import startup, shutdown

# import routes
from starlette.routing import Mount
from app.routes import index, account

# import exception handlers
from app.exceptions import error_403, error_404, error_500


def init_app():
    routes = [
        Mount('/static', StaticFiles(directory=STATIC_PATH), name='static'),
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

    app = App(
        debug=DEBUG, 
        routes=routes, 
        middleware=middlewares, 
        exception_handlers=exception_handlers,
        on_startup=[startup],
        on_shutdown=[shutdown]
    )

    return app
