"""
This module handles settings for the app
"""

import os
import pathlib
from starlette.config import Config
from starlette.datastructures import Secret, URL

# configure base root
BASE_ROOT = pathlib.Path(__file__).parent.parent

# configure template root
TEMPLATE_ROOT = os.path.join(BASE_ROOT, 'templates')

# configure static files root
STATIC_ROOT = os.path.join(BASE_ROOT, 'static')

# app's configuration
env_file = os.path.abspath(BASE_ROOT)
config = Config(env_file=f'{env_file}/.env')
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret, default=None)
HOST = config('HOST', cast=str, default='localhost')
PORT = config('PORT', cast=int, default=8000)

# app's database configuration
DB_URL = config('DB_URL', cast=URL, default='sqlite:///:memory:')
