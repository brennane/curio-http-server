from curio import run
from curio_http_server.handlers import Jinja2HandlerBase
from curio_http_server.handlers import jinja2_template
from curio_http_server.router import Router
from curio_http_server.server11 import Server11
from curio_http_server.forms import FormBase
from curio_http_server.forms import BooleanInput
from curio_http_server.forms import CharInput
from curio_http_server.forms import DateInput
from curio_http_server.forms import DecimalInput
from curio_http_server.forms import DropDownInput
from curio_http_server.forms import FileInput
from curio_http_server.forms import IntegerInput
from curio_http_server.forms import PasswordInput
from curio_http_server.forms import SlugInput
from curio_http_server.forms import TextInput
from curio_http_server.forms import TimeInput
from curio_http_server.forms import UUIDInput
from curio_http_server.forms import UrlInput
from jinja2 import Environment
from jinja2 import FileSystemLoader
from datetime import datetime
from os.path import dirname


class TestForm(FormBase):
    text = CharInput()
    password = PasswordInput()
    radio = SlugInput(choices={'A': 'radio A', 'B': 'radio B', 'C': 'radio C'})
    checkbox = BooleanInput(is_nullable=True)
    color = CharInput()
    date = DateInput()
    file = FileInput()
    number = DecimalInput()
    range = CharInput()
    time = TimeInput()
    url = UrlInput()

class DefaultHandler(Jinja2HandlerBase):
    def __init__(self):
        # Jinja2HandlerBase.__init__ will perform all kinds of black magic.
        super().__init__(Environment(
            loader=FileSystemLoader(dirname(__file__)),
            # Always enable async.
            enable_async=True))

    @jinja2_template('test_forms.html')
    async def get(self, request, response):
        return {}

    @jinja2_template('test_forms.html')
    async def post(self, request, response):
        data = await request.read_form()
        form = TestForm(prefix='post-2-')
        form.update(data)

        print()

        if not form.validate():
            print(form.data)
            print(form.errors)
        else:
            print(form.data)

        return {}

router = Router()
router.add('/', DefaultHandler())

# HTTP 1.1 server
server = Server11(
    router,
    default_headers=(('Server', 'curio-http-server/1.2.3.4'),))

print('Open the following URL with browser: http://localhost:8080/')

run(server.run(port=8080), with_monitor=True)
