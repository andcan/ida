"""
This type stub file was generated by pyright.
"""

from tornado import gen, httputil

"""Client and server implementations of HTTP/1.x.

.. versionadded:: 4.0
"""
class _QuietException(Exception):
    def __init__(self) -> None:
        ...
    


class _ExceptionLoggingContext(object):
    """Used with the ``with`` statement when calling delegate methods to
    log any exceptions with the given logger.  Any exceptions caught are
    converted to _QuietException
    """
    def __init__(self, logger) -> None:
        ...
    
    def __enter__(self):
        ...
    
    def __exit__(self, typ, value, tb):
        ...
    


class HTTP1ConnectionParameters(object):
    """Parameters for `.HTTP1Connection` and `.HTTP1ServerConnection`.
    """
    def __init__(self, no_keep_alive=..., chunk_size=..., max_header_size=..., header_timeout=..., max_body_size=..., body_timeout=..., decompress=...) -> None:
        """
        :arg bool no_keep_alive: If true, always close the connection after
            one request.
        :arg int chunk_size: how much data to read into memory at once
        :arg int max_header_size:  maximum amount of data for HTTP headers
        :arg float header_timeout: how long to wait for all headers (seconds)
        :arg int max_body_size: maximum amount of data for body
        :arg float body_timeout: how long to wait while reading body (seconds)
        :arg bool decompress: if true, decode incoming
            ``Content-Encoding: gzip``
        """
        ...
    


class HTTP1Connection(httputil.HTTPConnection):
    """Implements the HTTP/1.x protocol.

    This class can be on its own for clients, or via `HTTP1ServerConnection`
    for servers.
    """
    def __init__(self, stream, is_client, params=..., context=...) -> None:
        """
        :arg stream: an `.IOStream`
        :arg bool is_client: client or server
        :arg params: a `.HTTP1ConnectionParameters` instance or ``None``
        :arg context: an opaque application-defined object that can be accessed
            as ``connection.context``.
        """
        ...
    
    def read_response(self, delegate):
        """Read a single HTTP response.

        Typical client-mode usage is to write a request using `write_headers`,
        `write`, and `finish`, and then call ``read_response``.

        :arg delegate: a `.HTTPMessageDelegate`

        Returns a `.Future` that resolves to None after the full response has
        been read.
        """
        ...
    
    def set_close_callback(self, callback):
        """Sets a callback that will be run when the connection is closed.

        Note that this callback is slightly different from
        `.HTTPMessageDelegate.on_connection_close`: The
        `.HTTPMessageDelegate` method is called when the connection is
        closed while recieving a message. This callback is used when
        there is not an active delegate (for example, on the server
        side this callback is used if the client closes the connection
        after sending its request but before receiving all the
        response.
        """
        ...
    
    def close(self):
        ...
    
    def detach(self):
        """Take control of the underlying stream.

        Returns the underlying `.IOStream` object and stops all further
        HTTP processing.  May only be called during
        `.HTTPMessageDelegate.headers_received`.  Intended for implementing
        protocols like websockets that tunnel over an HTTP handshake.
        """
        ...
    
    def set_body_timeout(self, timeout):
        """Sets the body timeout for a single request.

        Overrides the value from `.HTTP1ConnectionParameters`.
        """
        ...
    
    def set_max_body_size(self, max_body_size):
        """Sets the body size limit for a single request.

        Overrides the value from `.HTTP1ConnectionParameters`.
        """
        ...
    
    def write_headers(self, start_line, headers, chunk=..., callback=...):
        """Implements `.HTTPConnection.write_headers`."""
        ...
    
    def write(self, chunk, callback=...):
        """Implements `.HTTPConnection.write`.

        For backwards compatibility it is allowed but deprecated to
        skip `write_headers` and instead call `write()` with a
        pre-encoded header block.
        """
        ...
    
    def finish(self):
        """Implements `.HTTPConnection.finish`."""
        ...
    


class _GzipMessageDelegate(httputil.HTTPMessageDelegate):
    """Wraps an `HTTPMessageDelegate` to decode ``Content-Encoding: gzip``.
    """
    def __init__(self, delegate, chunk_size) -> None:
        ...
    
    def headers_received(self, start_line, headers):
        ...
    
    @gen.coroutine
    def data_received(self, chunk):
        ...
    
    def finish(self):
        ...
    
    def on_connection_close(self):
        ...
    


class HTTP1ServerConnection(object):
    """An HTTP/1.x server."""
    def __init__(self, stream, params=..., context=...) -> None:
        """
        :arg stream: an `.IOStream`
        :arg params: a `.HTTP1ConnectionParameters` or None
        :arg context: an opaque application-defined object that is accessible
            as ``connection.context``
        """
        ...
    
    @gen.coroutine
    def close(self):
        """Closes the connection.

        Returns a `.Future` that resolves after the serving loop has exited.
        """
        ...
    
    def start_serving(self, delegate):
        """Starts serving requests on this connection.

        :arg delegate: a `.HTTPServerConnectionDelegate`
        """
        ...
    


