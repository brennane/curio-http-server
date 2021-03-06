from jinja2 import FileSystemLoader
from jinja2 import contextfilter
from os.path import dirname
from os.path import join


def jinja2_template(template_name):
    def jinja2_template_inner(function):
        function._template_name = template_name

        return function

    return jinja2_template_inner


def get_builtin_jinja2_loader():
    return FileSystemLoader(join(dirname(__file__), '../templates'))


@contextfilter
def render_macro(context, obj, module_name, macro_name, *args):
    module = context.vars.get(module_name)

    if not module:
        return f'"{module}" cannot be found ({context.vars.keys()}).'

    macro = getattr(module, macro_name)

    if not module:
        return f'"{module}.{macro_name}" cannot be found.'

    return macro(obj, *args)


class Jinja2HandlerBase(object):
    async def _render_template(self, request, data):
        pass

    def _get_wrapper(self, original_function):
        async def wrapper(request, response, *args, **kwargs):
            template = self._environment.get_template(original_function._template_name)
            result = await original_function(request, response, *args, **kwargs)
            html = await template.render_async(result)

            await response.send_html(html)

        return wrapper

    def __init__(self, environment):
        self._environment = environment
        self._environment.filters['render_macro'] = render_macro

        for method_name in ('connect', 'delete', 'get', 'head', 'options', 'patch', 'post', 'put', 'trace'):
            method = getattr(self, method_name, None)

            if callable(method) and hasattr(method, '_template_name'):
                setattr(self, method_name, self._get_wrapper(method))
