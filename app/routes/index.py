"""
This module serves as an index controller
"""

from starlette.requests import Request
from starlette.routing import Router, Route
from app.resources import template, template_env


async def home(request: Request):
    page = template_env.get_template('home.html')
    context = {'request': request}
    return template.TemplateResponse(page, context=context)


async def about(request: Request):
    page = template_env.get_template('about.html')
    context = {'request': request}
    return template.TemplateResponse(page, context=context)


routes = [
    Route('/', endpoint=home, methods=['GET', 'POST']),
    Route('/about', endpoint=about, methods=['GET'])
]
