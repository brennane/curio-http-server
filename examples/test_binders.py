from curio import run
from curio_http_server.binders import CheckboxInput
from curio_http_server.binders import ColorInput
from curio_http_server.binders import DateInput
from curio_http_server.binders import DateTimeInput
from curio_http_server.binders import EMailInput
from curio_http_server.binders import FileInput
from curio_http_server.binders import BinderBase
from curio_http_server.binders import HiddenInput
from curio_http_server.binders import NumberInput
from curio_http_server.binders import PasswordInput
from curio_http_server.binders import RadioInput
from curio_http_server.binders import SearchInput
from curio_http_server.binders import SelectInput
from curio_http_server.binders import TextInput
from curio_http_server.binders import TimeInput
from curio_http_server.binders import UrlInput
from curio_http_server.handlers.static import StaticHandler
from curio_http_server.handlers.template import Jinja2HandlerBase
from curio_http_server.handlers.template import get_builtin_jinja2_loader
from curio_http_server.handlers.template import jinja2_template
from curio_http_server.handlers.template import jinja2_template
from curio_http_server.router import Router
from curio_http_server.server11 import Server11
from datetime import date
from datetime import datetime
from datetime import timedelta
from jinja2 import ChoiceLoader
from jinja2 import Environment
from jinja2 import FileSystemLoader
from os.path import dirname
from os.path import join


class TestBinder(BinderBase):
    checkbox = CheckboxInput(
        verbose_name='Test Checkbox',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    color = ColorInput(
        verbose_name='Test Color Picker',
        help_text="Some help text here to give user an advice.")
    date = DateInput(
        min_value=(date.today() - timedelta(days=15)),
        max_value=(date.today() + timedelta(days=15)),
        verbose_name='Test Date Picker',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    datetime = DateTimeInput(
        min_value=(datetime.now() - timedelta(days=15)),
        max_value=(datetime.now() + timedelta(days=15)),
        verbose_name='Test Date and Time Picker',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    email = EMailInput(
        verbose_name='Test Email',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    file = FileInput(
        verbose_name='Test File',
        help_text="Some help text here to give user an advice.")
    hidden = HiddenInput(
        verbose_name='Test Hidden',
        help_text="Some help text here to give user an advice.")
    number = NumberInput(
        verbose_name='Test Number',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    password = PasswordInput(
        verbose_name='Test Password',
        help_text="Some help text here to give user an advice.")
    radio = RadioInput(
        verbose_name='Test Radio',
        choices={'A': 'radio A', 'B': 'radio B', 'C': 'radio C'},
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    search = SearchInput(
        verbose_name='Test Search',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    select = SelectInput(
        verbose_name='Test Select',
        choices={'': 'Select Something', 'X': 'select X', 'Y': 'select Y', 'Z': 'select Z'},
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    text = TextInput(
        verbose_name='Test Text',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    time = TimeInput(
        verbose_name='Test Time Picker',
        help_text="Some help text here to give user an advice.",
        can_filter=True)
    url = UrlInput(
        verbose_name='Test Url',
        help_text="Some help text here to give user an advice.",
        can_filter=True)


class DefaultHandler(Jinja2HandlerBase):
    def __init__(self):
        # Jinja2HandlerBase.__init__ will perform all kinds of black magic.
        super().__init__(Environment(
            loader=ChoiceLoader([
                get_builtin_jinja2_loader(),
                FileSystemLoader(dirname(__file__))
            ]),
            # Always enable async.
            enable_async=True))

    @jinja2_template('test_binders.html')
    async def get(self, request, response):
        binder1 = TestBinder(prefix='post-2-')

        return { 'binder1': binder1 }

    @jinja2_template('test_binders.html')
    async def post(self, request, response):
        data = await request.read_form()
        binder1 = TestBinder(prefix='post-2-')
        binder1._update(data)
        binder1._validate_item_update()

        print()
        print('data', binder1._data)
        print('errors', binder1._errors)

        return { 'binder1': binder1 }

router = Router()
router.add('/', DefaultHandler())
router.add('/static/<path:path>', StaticHandler(join(dirname(__file__), 'static')))

# HTTP 1.1 server
server = Server11(
    router,
    default_headers=(('Server', 'curio-http-server/1.2.3.4'),))

print('Open the following URL with browser: http://localhost:8080/')

run(server.run(port=8080), with_monitor=True)
