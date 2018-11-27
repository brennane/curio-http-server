from curio import run
from curio_http_server.handlers import Jinja2HandlerBase
from curio_http_server.handlers import jinja2_template
from curio_http_server.router import Router
from curio_http_server.server11 import Server11
from jinja2 import Environment
from jinja2 import FileSystemLoader
from datetime import datetime
from os.path import dirname


class DefaultHandler(Jinja2HandlerBase):
    def __init__(self):
        # Jinja2HandlerBase.__init__ will perform all kinds of black magic.
        super().__init__(Environment(
            loader=FileSystemLoader(dirname(__file__)),
            # Always enable async.
            enable_async=True))

    @jinja2_template('jinja2_handler.html')
    async def get(self, request, response):
        # Note that handler returns data
        return { 'size': 123456789, 'time': datetime.now()}

router = Router()
router.add('/', DefaultHandler())

# HTTP 1.1 server
server = Server11(
    router,
    default_headers=(('Server', 'curio-http-server/1.2.3.4'),))

print('Execute the following commands to test:')
print('curl -i http://localhost:8080/')

run(server.run(port=8080), with_monitor=True)
