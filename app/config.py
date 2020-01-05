"""
This module handles settings for the app
"""

import os
import pathlib
from starlette.config import Config
from starlette.datastructures import Secret, URL
from app.resources import BASE_PATH

# app's configuration
env_file = os.path.abspath(BASE_PATH)
config = Config(env_file=f'{env_file}/.env')
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret, default=None)
HOST = config('HOST', cast=str, default='localhost')
PORT = config('PORT', cast=int, default=8000)

# app's database configuration
DB_URL = config('DB_URL', cast=URL, default='sqlite:///:memory:')
