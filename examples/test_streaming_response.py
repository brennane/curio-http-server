from curio import run
from curio import sleep
from curio_http_server.core.router import Router
from curio_http_server.core.server11 import Server11


async def default_handler(request, response):
    # "Transfer-Encoding" will be "chunked" since we do not know content length
    # You cannot mix send_text, send_body, etc. with open_body!
    # Sending of Trailing headers is NOT supported yet. Sorry.
    async with response.open_body() as stream:
        for i in range(0, 1000):
            # Stream is not seekable, client will receive data as incrementally.
            # You MUST write binary data.
            # Each write call will produce separate chunk, so accumulate data wisely.
            # Chunk overhead is:
            #     5 bytes for chunks up to    15 bytes (33.3%, not a good idea)
            #     6 bytes for chunks up to   255 bytes ( 2.4%, mostly acceptable)
            #     7 bytes for chunks up to  4095 bytes ( 0.1%, very good)
            #     8 bytes for chunks up to 65535 bytes (absolutely negligible)
            await stream.write(b'%04d 0123456789\n' % i)

            # Slow down a bit so you can watch incremental download
            if i % 25 == 0:
                await sleep(1)

router = Router()
router.add('/', default_handler, 'GET')

# HTTP 1.1 server
server = Server11(
    router,
    default_headers=(('Server', 'curio-http-server/1.2.3.4'),))

print('Execute the following commands to test:')
print('curl -i -X GET http://localhost:8080/')

run(server.run(port=8080), with_monitor=True)
