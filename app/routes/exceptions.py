from app.views import template_env, template


async def error_403(request, exception):
    page = template_env.get_template('error_403.html')
    context = {'request': request}
    return template.TemplateResponse(html, context=context, status_code=400)


async def error_404(request, exception):
    page = template_env.get_template('error_404.html')
    context = {'request': request}
    return template.TemplateResponse(html, context=context, status_code=400)


async def error_500(request, exception):
    page = template_env.get_template('error_500.html')
    context = {'request': request}
    return template.TemplateResponse(html, context=context, status_code=500)