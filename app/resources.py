"""
This module handles the html pages to render from routes
"""

import os
import pathlib
from starlette.templating import Jinja2Templates as Templates
from jinja2 import FileSystemLoader

# configure base root
BASE_PATH = pathlib.Path(__file__).parent.parent

# configure static files root
STATIC_PATH = os.path.join(BASE_PATH, 'static')

# configure template root
template_dir = os.path.join(BASE_PATH, 'templates')

template = Templates(directory=template_dir)
template_env = template.get_env(template_dir)
template_env.loader = FileSystemLoader([
    f'{template_dir}',
    f'{template_dir}/account',
    f'{template_dir}/exceptions',
    f'{template_dir}/index',
    f'{template_dir}/shared'
])
