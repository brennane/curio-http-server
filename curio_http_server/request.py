from .headers import RequestHeaders
from curio import Event
from httptools import HttpRequestParser
from httptools import parse_url
from json import loads
from multidict import CIMultiDict
from urllib.parse import parse_qs


class RequestBodyStream(object):
    def __init__(self, request):
        self.request = request

    async def read(self):
        return await self.request._protocol.read_request()

    async def readall(self):
        body = b''
        content_length = self.request.headers.get('Content-Length')

        if content_length is not None:
            content_length = int(content_length) + 1

            while len(body) < content_length:
                data = await self.request._read_body()

                if not data:
                    break

                body +=  data
        else:
            while True:
                data = await self.request._read_body()

                if not data:
                    break

                body +=  data

        return body


class RequestBodyStreamContext(object):
    def __init__(self, request):
        self.request = request
        self.stream = RequestBodyStream(self.request)

    async def __aenter__(self):
        return self.stream

    async def __aexit__(self, exc_type, exc, tb):
        pass


class Request(object):
    def on_message_begin(self):
        pass

    def on_url(self, url: bytes):
        self.raw_path += url

    def on_header(self, name: bytes, value: bytes):
        str_name = name.decode('ascii')
        str_value = value.decode('ascii')

        self.raw_headers.add(str_name, value)
        self.headers.add(str_name, str_value)

    def on_headers_complete(self):
        parsed_path = parse_url(self.raw_path)

        self.version = self._parser.get_http_version()
        self.keep_alive = self._parser.should_keep_alive()
        self.upgrade = self._parser.should_upgrade()
        self.raw_method = self._parser.get_method()
        self.method = self.raw_method.decode('ascii')
        self.path = parsed_path.path.decode('ascii')

        for name, values in parse_qs(parsed_path.query).items():
            for value in values:
                self.raw_query.add(name.decode('ascii'), value)
                self.query.add(name.decode('ascii'), value.decode('ascii'))

        self._postprocess_headers()
        self._headers_complete = True

    def on_body(self, body: bytes):
        self._body_buffer += body

    def on_message_complete(self):
        self._body_complete = True

    def on_chunk_header(self):
        pass

    def on_chunk_complete(self):
        pass

    async def _try_read_headers(self):
        while not self._headers_complete:
            data = await self._connection.read_request()

            if not data:
                return False

            self._parser.feed_data(data)

        return True

    async def _read_body(self):
        while not self._body_complete:
            data = await self._connection.read_request()

            if not data:
                self._body_complete = True
                return b''

            self._parser.feed_data(data)

            if len(self._body_buffer) > 0:
                result = self._body_buffer
                self._body_buffer = b''

                return result

        return b''

    def _postprocess_headers(self):
        self.headers._post_process(self)

    def __init__(self, connection):
        self._connection = connection
        self._parser = HttpRequestParser(self)
        self._body_buffer = b''
        self._headers_complete = False
        self._body_complete = False

        self.version = None
        self.keep_alive = None
        self.upgrade = None
        self.address = connection.address
        self.raw_method = b''
        self.raw_headers = CIMultiDict()
        self.raw_query = CIMultiDict()
        self.raw_path = b''

        self.method = ''
        self.host = 'localhost'
        self.port = 80
        self.headers = RequestHeaders()
        self.query = CIMultiDict()
        self.cookies = {}
        self.path = ''
        self.content_type_main = 'application'
        self.content_type_sub = 'octet-stream'
        self.content_type_params = {}
        self.content_charset = 'ascii'

        self._is_body_complete = False
        self._body = None
        self._text = None
        self._json = None
        self._form = None

    async def read_body(self):
        if self._body is None:
            async with self.open_body() as stream:
                self._body = await stream.readall()

        return self._body

    async def read_text(self):
        if self._text is None:
            charset = self.content_type_params.get('charset', 'ascii')

            self._text = self.read_body().decode(charset)

        return self._text

    async def read_json(self):
        if self._json is None:
            self._json = loads(self.read_text())

        return self._json

    async def read_form(self):
        if self._form is None:
            self._form = CIMultiDict()

            for name, values in parse_qs(self.read_body()).items():
                for value in values:
                    self._form.add(name.decode('utf-8'), value.decode('utf-8'))

        return self._form

    def open_body(self):
        return RequestBodyStreamContext(self)
