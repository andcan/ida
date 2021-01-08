"""
This type stub file was generated by pyright.
"""

from tornado import gen, httputil
from tornado.tcpserver import TCPServer
from tornado.util import Configurable

"""A non-blocking, single-threaded HTTP server.

Typical applications have little direct interaction with the `HTTPServer`
class except to start a server at the beginning of the process
(and even that is often done indirectly via `tornado.web.Application.listen`).

.. versionchanged:: 4.0

   The ``HTTPRequest`` class that used to live in this module has been moved
   to `tornado.httputil.HTTPServerRequest`.  The old name remains as an alias.
"""
class HTTPServer(TCPServer, Configurable, httputil.HTTPServerConnectionDelegate):
    r"""A non-blocking, single-threaded HTTP server.

    A server is defined by a subclass of `.HTTPServerConnectionDelegate`,
    or, for backwards compatibility, a callback that takes an
    `.HTTPServerRequest` as an argument. The delegate is usually a
    `tornado.web.Application`.

    `HTTPServer` supports keep-alive connections by default
    (automatically for HTTP/1.1, or for HTTP/1.0 when the client
    requests ``Connection: keep-alive``).

    If ``xheaders`` is ``True``, we support the
    ``X-Real-Ip``/``X-Forwarded-For`` and
    ``X-Scheme``/``X-Forwarded-Proto`` headers, which override the
    remote IP and URI scheme/protocol for all requests.  These headers
    are useful when running Tornado behind a reverse proxy or load
    balancer.  The ``protocol`` argument can also be set to ``https``
    if Tornado is run behind an SSL-decoding proxy that does not set one of
    the supported ``xheaders``.

    By default, when parsing the ``X-Forwarded-For`` header, Tornado will
    select the last (i.e., the closest) address on the list of hosts as the
    remote host IP address.  To select the next server in the chain, a list of
    trusted downstream hosts may be passed as the ``trusted_downstream``
    argument.  These hosts will be skipped when parsing the ``X-Forwarded-For``
    header.

    To make this server serve SSL traffic, send the ``ssl_options`` keyword
    argument with an `ssl.SSLContext` object. For compatibility with older
    versions of Python ``ssl_options`` may also be a dictionary of keyword
    arguments for the `ssl.wrap_socket` method.::

       ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
       ssl_ctx.load_cert_chain(os.path.join(data_dir, "mydomain.crt"),
                               os.path.join(data_dir, "mydomain.key"))
       HTTPServer(application, ssl_options=ssl_ctx)

    `HTTPServer` initialization follows one of three patterns (the
    initialization methods are defined on `tornado.tcpserver.TCPServer`):

    1. `~tornado.tcpserver.TCPServer.listen`: simple single-process::

            server = HTTPServer(app)
            server.listen(8888)
            IOLoop.current().start()

       In many cases, `tornado.web.Application.listen` can be used to avoid
       the need to explicitly create the `HTTPServer`.

    2. `~tornado.tcpserver.TCPServer.bind`/`~tornado.tcpserver.TCPServer.start`:
       simple multi-process::

            server = HTTPServer(app)
            server.bind(8888)
            server.start(0)  # Forks multiple sub-processes
            IOLoop.current().start()

       When using this interface, an `.IOLoop` must *not* be passed
       to the `HTTPServer` constructor.  `~.TCPServer.start` will always start
       the server on the default singleton `.IOLoop`.

    3. `~tornado.tcpserver.TCPServer.add_sockets`: advanced multi-process::

            sockets = tornado.netutil.bind_sockets(8888)
            tornado.process.fork_processes(0)
            server = HTTPServer(app)
            server.add_sockets(sockets)
            IOLoop.current().start()

       The `~.TCPServer.add_sockets` interface is more complicated,
       but it can be used with `tornado.process.fork_processes` to
       give you more flexibility in when the fork happens.
       `~.TCPServer.add_sockets` can also be used in single-process
       servers if you want to create your listening sockets in some
       way other than `tornado.netutil.bind_sockets`.

    .. versionchanged:: 4.0
       Added ``decompress_request``, ``chunk_size``, ``max_header_size``,
       ``idle_connection_timeout``, ``body_timeout``, ``max_body_size``
       arguments.  Added support for `.HTTPServerConnectionDelegate`
       instances as ``request_callback``.

    .. versionchanged:: 4.1
       `.HTTPServerConnectionDelegate.start_request` is now called with
       two arguments ``(server_conn, request_conn)`` (in accordance with the
       documentation) instead of one ``(request_conn)``.

    .. versionchanged:: 4.2
       `HTTPServer` is now a subclass of `tornado.util.Configurable`.

    .. versionchanged:: 4.5
       Added the ``trusted_downstream`` argument.

    .. versionchanged:: 5.0
       The ``io_loop`` argument has been removed.
    """
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def initialize(self, request_callback, no_keep_alive=..., xheaders=..., ssl_options=..., protocol=..., decompress_request=..., chunk_size=..., max_header_size=..., idle_connection_timeout=..., body_timeout=..., max_body_size=..., max_buffer_size=..., trusted_downstream=...):
        ...
    
    @classmethod
    def configurable_base(cls):
        ...
    
    @classmethod
    def configurable_default(cls):
        ...
    
    @gen.coroutine
    def close_all_connections(self):
        ...
    
    def handle_stream(self, stream, address):
        ...
    
    def start_request(self, server_conn, request_conn):
        ...
    
    def on_close(self, server_conn):
        ...
    


class _CallableAdapter(httputil.HTTPMessageDelegate):
    def __init__(self, request_callback, request_conn) -> None:
        ...
    
    def headers_received(self, start_line, headers):
        ...
    
    def data_received(self, chunk):
        ...
    
    def finish(self):
        ...
    
    def on_connection_close(self):
        ...
    


class _HTTPRequestContext(object):
    def __init__(self, stream, address, protocol, trusted_downstream=...) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    


class _ProxyAdapter(httputil.HTTPMessageDelegate):
    def __init__(self, delegate, request_conn) -> None:
        ...
    
    def headers_received(self, start_line, headers):
        ...
    
    def data_received(self, chunk):
        ...
    
    def finish(self):
        ...
    
    def on_connection_close(self):
        ...
    


HTTPRequest = httputil.HTTPServerRequest