#  Curio HTTP Server

[Curio](https://github.com/dabeaz/curio) based [HTTP server](https://en.wikipedia.org/wiki/Web_server) with [Jinja2](https://github.com/pallets/jinja) templates support.


Simplest usage looks like this

```python
from curio import run
from curio_http_server.core.router import Router
from curio_http_server.core.server11 import Server11

async def hello(request, response):
    await response.send_text('Hello!')

router = Router()
router.add('/', hello, 'GET')
server = Server11(router)

run(server.run(port=8080), with_monitor=True)
```

See [examples](https://github.com/triflesoft/curio-http-server/tree/master/examples) for advanced examples, including streaming responses, HTML forms, jinja templates and more.

See [Wiki](https://github.com/triflesoft/curio-http-server/wiki) for additional information.
