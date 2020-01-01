"""
This module serves to initialize the application factory
"""

from starlette.applications import Starlette
from starlette.routing import Router

# import application middlewares
from starlette.middleware.sessions import SessionMiddleware
from app.middlewares import RequestVerificationCookieMiddleware, RequestSessionVerificationMiddleware

# import static file class
from starlette.staticfiles import StaticFiles

# import app configurations
from app.config import DEBUG, STATIC_ROOT, SECRET_KEY

# import event handlers
from app.events import startup, shutdown

# import exception handlers
from app.routes.exceptions import error_403, error_404, error_500

# import application routes
from app.routes.index import index_router
from app.routes.account import account_router


def init_app():
    app = Starlette(debug=DEBUG)

    # add application middlewares
    app.add_middleware(RequestVerificationCookieMiddleware)
    app.add_middleware(RequestSessionVerificationMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    # add app event handlers
    app.add_event_handler('startup', startup)
    app.add_event_handler('shutdown', shutdown)

    # mount static files
    app.mount('/static', StaticFiles(directory=STATIC_ROOT), name='static')

    # mount exception handlers
    app.add_exception_handler(403, error_403)
    app.add_exception_handler(404, error_404)
    app.add_exception_handler(500, error_500)

    # mounting application routes
    app.mount('/account', account_router)
    app.mount('/', index_router)

    return app
