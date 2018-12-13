#!/usr/bin/env python3

from curio import run
from curio_http_server.core.router import Router
from curio_http_server.core.server11 import Server11


async def inner(request, response, a, b):
    await response.send_text(f'INNER {a} {b}')


router1 = Router()
router1.add('/<b:int>/', inner, 'GET')
router1.add('-<b:int>', inner, 'GET')

router2 = Router()
# note that one '/' will be collapsed so final path is '/<a:int>/<b:int>/', not '/<a:int>//<b:int>/'
router2.add('/<a:int>/', router1)
router2.add('/<a:int>', router1)

# HTTP 1.1 server
server = Server11(
    router2,
    default_headers=(('Server', 'curio-http-server/1.2.3.4'),))

print('Execute the following commands to test:')
print('curl -i http://localhost:8080/1/2/')
print('curl -i http://localhost:8080/1-2')

run(server.run(port=8080), with_monitor=True)
