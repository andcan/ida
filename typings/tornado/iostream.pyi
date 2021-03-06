"""
This type stub file was generated by pyright.
"""

import errno
import sys

"""Utility classes to write to and read from non-blocking files and sockets.

Contents:

* `BaseIOStream`: Generic interface for reading and writing.
* `IOStream`: Implementation of BaseIOStream using non-blocking sockets.
* `SSLIOStream`: SSL-aware version of IOStream.
* `PipeIOStream`: Pipe-based IOStream implementation.
"""
_ERRNO_WOULDBLOCK = (errno.EWOULDBLOCK, errno.EAGAIN)
if hasattr(errno, "WSAEWOULDBLOCK"):
    ...
_ERRNO_CONNRESET = (errno.ECONNRESET, errno.ECONNABORTED, errno.EPIPE, errno.ETIMEDOUT)
if hasattr(errno, "WSAECONNRESET"):
    ...
if sys.platform == 'darwin':
    ...
_ERRNO_INPROGRESS = (errno.EINPROGRESS, )
if hasattr(errno, "WSAEINPROGRESS"):
    ...
_WINDOWS = sys.platform.startswith('win')
class StreamClosedError(IOError):
    """Exception raised by `IOStream` methods when the stream is closed.

    Note that the close callback is scheduled to run *after* other
    callbacks on the stream (to allow for buffered data to be processed),
    so you may see this error before you see the close callback.

    The ``real_error`` attribute contains the underlying error that caused
    the stream to close (if any).

    .. versionchanged:: 4.3
       Added the ``real_error`` attribute.
    """
    def __init__(self, real_error=...) -> None:
        ...
    


class UnsatisfiableReadError(Exception):
    """Exception raised when a read cannot be satisfied.

    Raised by ``read_until`` and ``read_until_regex`` with a ``max_bytes``
    argument.
    """
    ...


class StreamBufferFullError(Exception):
    """Exception raised by `IOStream` methods when the buffer is full.
    """
    ...


class _StreamBuffer(object):
    """
    A specialized buffer that tries to avoid copies when large pieces
    of data are encountered.
    """
    def __init__(self) -> None:
        ...
    
    def __len__(self):
        ...
    
    _large_buf_threshold = ...
    def append(self, data):
        """
        Append the given piece of data (should be a buffer-compatible object).
        """
        ...
    
    def peek(self, size):
        """
        Get a view over at most ``size`` bytes (possibly fewer) at the
        current buffer position.
        """
        ...
    
    def advance(self, size):
        """
        Advance the current buffer position by ``size`` bytes.
        """
        ...
    


class BaseIOStream(object):
    """A utility class to write to and read from a non-blocking file or socket.

    We support a non-blocking ``write()`` and a family of ``read_*()`` methods.
    All of the methods take an optional ``callback`` argument and return a
    `.Future` only if no callback is given.  When the operation completes,
    the callback will be run or the `.Future` will resolve with the data
    read (or ``None`` for ``write()``).  All outstanding ``Futures`` will
    resolve with a `StreamClosedError` when the stream is closed; users
    of the callback interface will be notified via
    `.BaseIOStream.set_close_callback` instead.

    When a stream is closed due to an error, the IOStream's ``error``
    attribute contains the exception object.

    Subclasses must implement `fileno`, `close_fd`, `write_to_fd`,
    `read_from_fd`, and optionally `get_fd_error`.
    """
    def __init__(self, max_buffer_size=..., read_chunk_size=..., max_write_buffer_size=...) -> None:
        """`BaseIOStream` constructor.

        :arg max_buffer_size: Maximum amount of incoming data to buffer;
            defaults to 100MB.
        :arg read_chunk_size: Amount of data to read at one time from the
            underlying transport; defaults to 64KB.
        :arg max_write_buffer_size: Amount of outgoing data to buffer;
            defaults to unlimited.

        .. versionchanged:: 4.0
           Add the ``max_write_buffer_size`` parameter.  Changed default
           ``read_chunk_size`` to 64KB.
        .. versionchanged:: 5.0
           The ``io_loop`` argument (deprecated since version 4.1) has been
           removed.
        """
        ...
    
    def fileno(self):
        """Returns the file descriptor for this stream."""
        ...
    
    def close_fd(self):
        """Closes the file underlying this stream.

        ``close_fd`` is called by `BaseIOStream` and should not be called
        elsewhere; other users should call `close` instead.
        """
        ...
    
    def write_to_fd(self, data):
        """Attempts to write ``data`` to the underlying file.

        Returns the number of bytes written.
        """
        ...
    
    def read_from_fd(self, buf):
        """Attempts to read from the underlying file.

        Reads up to ``len(buf)`` bytes, storing them in the buffer.
        Returns the number of bytes read. Returns None if there was
        nothing to read (the socket returned `~errno.EWOULDBLOCK` or
        equivalent), and zero on EOF.

        .. versionchanged:: 5.0

           Interface redesigned to take a buffer and return a number
           of bytes instead of a freshly-allocated object.
        """
        ...
    
    def get_fd_error(self):
        """Returns information about any error on the underlying file.

        This method is called after the `.IOLoop` has signaled an error on the
        file descriptor, and should return an Exception (such as `socket.error`
        with additional information, or None if no such information is
        available.
        """
        ...
    
    def read_until_regex(self, regex, callback=..., max_bytes=...):
        """Asynchronously read until we have matched the given regex.

        The result includes the data that matches the regex and anything
        that came before it.  If a callback is given, it will be run
        with the data as an argument; if not, this method returns a
        `.Future`.

        If ``max_bytes`` is not None, the connection will be closed
        if more than ``max_bytes`` bytes have been read and the regex is
        not satisfied.

        .. versionchanged:: 4.0
            Added the ``max_bytes`` argument.  The ``callback`` argument is
            now optional and a `.Future` will be returned if it is omitted.

        .. deprecated:: 5.1

           The ``callback`` argument is deprecated and will be removed
           in Tornado 6.0. Use the returned `.Future` instead.

        """
        ...
    
    def read_until(self, delimiter, callback=..., max_bytes=...):
        """Asynchronously read until we have found the given delimiter.

        The result includes all the data read including the delimiter.
        If a callback is given, it will be run with the data as an argument;
        if not, this method returns a `.Future`.

        If ``max_bytes`` is not None, the connection will be closed
        if more than ``max_bytes`` bytes have been read and the delimiter
        is not found.

        .. versionchanged:: 4.0
            Added the ``max_bytes`` argument.  The ``callback`` argument is
            now optional and a `.Future` will be returned if it is omitted.

        .. deprecated:: 5.1

           The ``callback`` argument is deprecated and will be removed
           in Tornado 6.0. Use the returned `.Future` instead.
        """
        ...
    
    def read_bytes(self, num_bytes, callback=..., streaming_callback=..., partial=...):
        """Asynchronously read a number of bytes.

        If a ``streaming_callback`` is given, it will be called with chunks
        of data as they become available, and the final result will be empty.
        Otherwise, the result is all the data that was read.
        If a callback is given, it will be run with the data as an argument;
        if not, this method returns a `.Future`.

        If ``partial`` is true, the callback is run as soon as we have
        any bytes to return (but never more than ``num_bytes``)

        .. versionchanged:: 4.0
            Added the ``partial`` argument.  The callback argument is now
            optional and a `.Future` will be returned if it is omitted.

        .. deprecated:: 5.1

           The ``callback`` and ``streaming_callback`` arguments are
           deprecated and will be removed in Tornado 6.0. Use the
           returned `.Future` (and ``partial=True`` for
           ``streaming_callback``) instead.

        """
        ...
    
    def read_into(self, buf, callback=..., partial=...):
        """Asynchronously read a number of bytes.

        ``buf`` must be a writable buffer into which data will be read.
        If a callback is given, it will be run with the number of read
        bytes as an argument; if not, this method returns a `.Future`.

        If ``partial`` is true, the callback is run as soon as any bytes
        have been read.  Otherwise, it is run when the ``buf`` has been
        entirely filled with read data.

        .. versionadded:: 5.0

        .. deprecated:: 5.1

           The ``callback`` argument is deprecated and will be removed
           in Tornado 6.0. Use the returned `.Future` instead.

        """
        ...
    
    def read_until_close(self, callback=..., streaming_callback=...):
        """Asynchronously reads all data from the socket until it is closed.

        If a ``streaming_callback`` is given, it will be called with chunks
        of data as they become available, and the final result will be empty.
        Otherwise, the result is all the data that was read.
        If a callback is given, it will be run with the data as an argument;
        if not, this method returns a `.Future`.

        Note that if a ``streaming_callback`` is used, data will be
        read from the socket as quickly as it becomes available; there
        is no way to apply backpressure or cancel the reads. If flow
        control or cancellation are desired, use a loop with
        `read_bytes(partial=True) <.read_bytes>` instead.

        .. versionchanged:: 4.0
            The callback argument is now optional and a `.Future` will
            be returned if it is omitted.

        .. deprecated:: 5.1

           The ``callback`` and ``streaming_callback`` arguments are
           deprecated and will be removed in Tornado 6.0. Use the
           returned `.Future` (and `read_bytes` with ``partial=True``
           for ``streaming_callback``) instead.

        """
        ...
    
    def write(self, data, callback=...):
        """Asynchronously write the given data to this stream.

        If ``callback`` is given, we call it when all of the buffered write
        data has been successfully written to the stream. If there was
        previously buffered write data and an old write callback, that
        callback is simply overwritten with this new callback.

        If no ``callback`` is given, this method returns a `.Future` that
        resolves (with a result of ``None``) when the write has been
        completed.

        The ``data`` argument may be of type `bytes` or `memoryview`.

        .. versionchanged:: 4.0
            Now returns a `.Future` if no callback is given.

        .. versionchanged:: 4.5
            Added support for `memoryview` arguments.

        .. deprecated:: 5.1

           The ``callback`` argument is deprecated and will be removed
           in Tornado 6.0. Use the returned `.Future` instead.

        """
        ...
    
    def set_close_callback(self, callback):
        """Call the given callback when the stream is closed.

        This mostly is not necessary for applications that use the
        `.Future` interface; all outstanding ``Futures`` will resolve
        with a `StreamClosedError` when the stream is closed. However,
        it is still useful as a way to signal that the stream has been
        closed while no other read or write is in progress.

        Unlike other callback-based interfaces, ``set_close_callback``
        will not be removed in Tornado 6.0.
        """
        ...
    
    def close(self, exc_info=...):
        """Close this stream.

        If ``exc_info`` is true, set the ``error`` attribute to the current
        exception from `sys.exc_info` (or if ``exc_info`` is a tuple,
        use that instead of `sys.exc_info`).
        """
        ...
    
    def reading(self):
        """Returns true if we are currently reading from the stream."""
        ...
    
    def writing(self):
        """Returns true if we are currently writing to the stream."""
        ...
    
    def closed(self):
        """Returns true if the stream has been closed."""
        ...
    
    def set_nodelay(self, value):
        """Sets the no-delay flag for this stream.

        By default, data written to TCP streams may be held for a time
        to make the most efficient use of bandwidth (according to
        Nagle's algorithm).  The no-delay flag requests that data be
        written as soon as possible, even if doing so would consume
        additional bandwidth.

        This flag is currently defined only for TCP-based ``IOStreams``.

        .. versionadded:: 3.1
        """
        ...
    


class IOStream(BaseIOStream):
    r"""Socket-based `IOStream` implementation.

    This class supports the read and write methods from `BaseIOStream`
    plus a `connect` method.

    The ``socket`` parameter may either be connected or unconnected.
    For server operations the socket is the result of calling
    `socket.accept <socket.socket.accept>`.  For client operations the
    socket is created with `socket.socket`, and may either be
    connected before passing it to the `IOStream` or connected with
    `IOStream.connect`.

    A very simple (and broken) HTTP client using this class:

    .. testcode::

        import tornado.ioloop
        import tornado.iostream
        import socket

        async def main():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            stream = tornado.iostream.IOStream(s)
            await stream.connect(("friendfeed.com", 80))
            await stream.write(b"GET / HTTP/1.0\r\nHost: friendfeed.com\r\n\r\n")
            header_data = await stream.read_until(b"\r\n\r\n")
            headers = {}
            for line in header_data.split(b"\r\n"):
                parts = line.split(b":")
                if len(parts) == 2:
                    headers[parts[0].strip()] = parts[1].strip()
            body_data = await stream.read_bytes(int(headers[b"Content-Length"]))
            print(body_data)
            stream.close()

        if __name__ == '__main__':
            tornado.ioloop.IOLoop.current().run_sync(main)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            stream = tornado.iostream.IOStream(s)
            stream.connect(("friendfeed.com", 80), send_request)
            tornado.ioloop.IOLoop.current().start()

    .. testoutput::
       :hide:

    """
    def __init__(self, socket, *args, **kwargs) -> None:
        ...
    
    def fileno(self):
        ...
    
    def close_fd(self):
        ...
    
    def get_fd_error(self):
        ...
    
    def read_from_fd(self, buf):
        ...
    
    def write_to_fd(self, data):
        ...
    
    def connect(self, address, callback=..., server_hostname=...):
        """Connects the socket to a remote address without blocking.

        May only be called if the socket passed to the constructor was
        not previously connected.  The address parameter is in the
        same format as for `socket.connect <socket.socket.connect>` for
        the type of socket passed to the IOStream constructor,
        e.g. an ``(ip, port)`` tuple.  Hostnames are accepted here,
        but will be resolved synchronously and block the IOLoop.
        If you have a hostname instead of an IP address, the `.TCPClient`
        class is recommended instead of calling this method directly.
        `.TCPClient` will do asynchronous DNS resolution and handle
        both IPv4 and IPv6.

        If ``callback`` is specified, it will be called with no
        arguments when the connection is completed; if not this method
        returns a `.Future` (whose result after a successful
        connection will be the stream itself).

        In SSL mode, the ``server_hostname`` parameter will be used
        for certificate validation (unless disabled in the
        ``ssl_options``) and SNI (if supported; requires Python
        2.7.9+).

        Note that it is safe to call `IOStream.write
        <BaseIOStream.write>` while the connection is pending, in
        which case the data will be written as soon as the connection
        is ready.  Calling `IOStream` read methods before the socket is
        connected works on some platforms but is non-portable.

        .. versionchanged:: 4.0
            If no callback is given, returns a `.Future`.

        .. versionchanged:: 4.2
           SSL certificates are validated by default; pass
           ``ssl_options=dict(cert_reqs=ssl.CERT_NONE)`` or a
           suitably-configured `ssl.SSLContext` to the
           `SSLIOStream` constructor to disable.

        .. deprecated:: 5.1

           The ``callback`` argument is deprecated and will be removed
           in Tornado 6.0. Use the returned `.Future` instead.

        """
        ...
    
    def start_tls(self, server_side, ssl_options=..., server_hostname=...):
        """Convert this `IOStream` to an `SSLIOStream`.

        This enables protocols that begin in clear-text mode and
        switch to SSL after some initial negotiation (such as the
        ``STARTTLS`` extension to SMTP and IMAP).

        This method cannot be used if there are outstanding reads
        or writes on the stream, or if there is any data in the
        IOStream's buffer (data in the operating system's socket
        buffer is allowed).  This means it must generally be used
        immediately after reading or writing the last clear-text
        data.  It can also be used immediately after connecting,
        before any reads or writes.

        The ``ssl_options`` argument may be either an `ssl.SSLContext`
        object or a dictionary of keyword arguments for the
        `ssl.wrap_socket` function.  The ``server_hostname`` argument
        will be used for certificate validation unless disabled
        in the ``ssl_options``.

        This method returns a `.Future` whose result is the new
        `SSLIOStream`.  After this method has been called,
        any other operation on the original stream is undefined.

        If a close callback is defined on this stream, it will be
        transferred to the new stream.

        .. versionadded:: 4.0

        .. versionchanged:: 4.2
           SSL certificates are validated by default; pass
           ``ssl_options=dict(cert_reqs=ssl.CERT_NONE)`` or a
           suitably-configured `ssl.SSLContext` to disable.
        """
        ...
    
    def set_nodelay(self, value):
        ...
    


class SSLIOStream(IOStream):
    """A utility class to write to and read from a non-blocking SSL socket.

    If the socket passed to the constructor is already connected,
    it should be wrapped with::

        ssl.wrap_socket(sock, do_handshake_on_connect=False, **kwargs)

    before constructing the `SSLIOStream`.  Unconnected sockets will be
    wrapped when `IOStream.connect` is finished.
    """
    def __init__(self, *args, **kwargs) -> None:
        """The ``ssl_options`` keyword argument may either be an
        `ssl.SSLContext` object or a dictionary of keywords arguments
        for `ssl.wrap_socket`
        """
        ...
    
    def reading(self):
        ...
    
    def writing(self):
        ...
    
    def connect(self, address, callback=..., server_hostname=...):
        ...
    
    def wait_for_handshake(self, callback=...):
        """Wait for the initial SSL handshake to complete.

        If a ``callback`` is given, it will be called with no
        arguments once the handshake is complete; otherwise this
        method returns a `.Future` which will resolve to the
        stream itself after the handshake is complete.

        Once the handshake is complete, information such as
        the peer's certificate and NPN/ALPN selections may be
        accessed on ``self.socket``.

        This method is intended for use on server-side streams
        or after using `IOStream.start_tls`; it should not be used
        with `IOStream.connect` (which already waits for the
        handshake to complete). It may only be called once per stream.

        .. versionadded:: 4.2

        .. deprecated:: 5.1

           The ``callback`` argument is deprecated and will be removed
           in Tornado 6.0. Use the returned `.Future` instead.

        """
        ...
    
    def write_to_fd(self, data):
        ...
    
    def read_from_fd(self, buf):
        ...
    


class PipeIOStream(BaseIOStream):
    """Pipe-based `IOStream` implementation.

    The constructor takes an integer file descriptor (such as one returned
    by `os.pipe`) rather than an open file object.  Pipes are generally
    one-way, so a `PipeIOStream` can be used for reading or writing but not
    both.
    """
    def __init__(self, fd, *args, **kwargs) -> None:
        ...
    
    def fileno(self):
        ...
    
    def close_fd(self):
        ...
    
    def write_to_fd(self, data):
        ...
    
    def read_from_fd(self, buf):
        ...
    


def doctests():
    ...

