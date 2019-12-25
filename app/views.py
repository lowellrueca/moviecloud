"""
This module handles the html pages to render from routes
"""

from starlette.templating import Jinja2Templates as Templates
from jinja2 import FileSystemLoader
from app.config import TEMPLATE_ROOT


template = Templates(directory=TEMPLATE_ROOT)
template_env = template.get_env(TEMPLATE_ROOT)
template_env.loader = FileSystemLoader([
    f'{TEMPLATE_ROOT}',
    f'{TEMPLATE_ROOT}/account',
    f'{TEMPLATE_ROOT}/exceptions',
    f'{TEMPLATE_ROOT}/index',
    f'{TEMPLATE_ROOT}/shared'
])
