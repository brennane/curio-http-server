from curio import run
from curio_http_server.core.router import Router
from curio_http_server.core.server11 import Server11


async def default_handler(request, response):
    await response.send_text('Handler executed.')


# If no handler matched, middlewares will not be executed.
# You can owerwrite handling in before()
# If you return True from before() the rest of middlewares as well as matched handler will not be executed.
# Always return True if you send body.
# You cannot change anything in after(), it's too late.
class Middleware(object):
    async def before(self, request, response):
        if request.method == 'POST':
            await response.send_text('Middleware intercepted POST request! Handler will not be executed!')
            return True

    async def after(self, request, response):
        pass


router = Router()
router.add('/', default_handler, ('GET', 'POST'))

# HTTP 1.1 server
# Note that middleware instances, not classes are passer to the server.
server = Server11(
    router,
    middlewares=(Middleware(),),
    default_headers=(('Server', 'curio-http-server/1.2.3.4'),))

print('Execute the following commands to test:')
print('curl -i -X GET http://localhost:8080/')
print('curl -i -X POST http://localhost:8080/')
print('curl -i -X POST http://localhost:8080/error/')

run(server.run(port=8080), with_monitor=True)
