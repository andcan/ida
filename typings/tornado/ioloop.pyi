"""
This type stub file was generated by pyright.
"""

from tornado.util import Configurable, PY3

"""An I/O event loop for non-blocking sockets.

On Python 3, `.IOLoop` is a wrapper around the `asyncio` event loop.

Typical applications will use a single `IOLoop` object, accessed via
`IOLoop.current` class method. The `IOLoop.start` method (or
equivalently, `asyncio.AbstractEventLoop.run_forever`) should usually
be called at the end of the ``main()`` function. Atypical applications
may use more than one `IOLoop`, such as one `IOLoop` per thread, or
per `unittest` case.

In addition to I/O events, the `IOLoop` can also schedule time-based
events. `IOLoop.add_timeout` is a non-blocking alternative to
`time.sleep`.

"""
if PY3:
    ...
else:
    ...
_POLL_TIMEOUT = 3600
class IOLoop(Configurable):
    """A level-triggered I/O loop.

    On Python 3, `IOLoop` is a wrapper around the `asyncio` event
    loop. On Python 2, it uses ``epoll`` (Linux) or ``kqueue`` (BSD
    and Mac OS X) if they are available, or else we fall back on
    select(). If you are implementing a system that needs to handle
    thousands of simultaneous connections, you should use a system
    that supports either ``epoll`` or ``kqueue``.

    Example usage for a simple TCP server:

    .. testcode::

        import errno
        import functools
        import socket

        import tornado.ioloop
        from tornado.iostream import IOStream

        async def handle_connection(connection, address):
            stream = IOStream(connection)
            message = await stream.read_until_close()
            print("message from client:", message.decode().strip())

        def connection_ready(sock, fd, events):
            while True:
                try:
                    connection, address = sock.accept()
                except socket.error as e:
                    if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                        raise
                    return
                connection.setblocking(0)
                io_loop = tornado.ioloop.IOLoop.current()
                io_loop.spawn_callback(handle_connection, connection, address)

        if __name__ == '__main__':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(0)
            sock.bind(("", 8888))
            sock.listen(128)

            io_loop = tornado.ioloop.IOLoop.current()
            callback = functools.partial(connection_ready, sock)
            io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
            io_loop.start()

    .. testoutput::
       :hide:

    By default, a newly-constructed `IOLoop` becomes the thread's current
    `IOLoop`, unless there already is a current `IOLoop`. This behavior
    can be controlled with the ``make_current`` argument to the `IOLoop`
    constructor: if ``make_current=True``, the new `IOLoop` will always
    try to become current and it raises an error if there is already a
    current instance. If ``make_current=False``, the new `IOLoop` will
    not try to become current.

    In general, an `IOLoop` cannot survive a fork or be shared across
    processes in any way. When multiple processes are being used, each
    process should create its own `IOLoop`, which also implies that
    any objects which depend on the `IOLoop` (such as
    `.AsyncHTTPClient`) must also be created in the child processes.
    As a guideline, anything that starts processes (including the
    `tornado.process` and `multiprocessing` modules) should do so as
    early as possible, ideally the first thing the application does
    after loading its configuration in ``main()``.

    .. versionchanged:: 4.2
       Added the ``make_current`` keyword argument to the `IOLoop`
       constructor.

    .. versionchanged:: 5.0

       Uses the `asyncio` event loop by default. The
       ``IOLoop.configure`` method cannot be used on Python 3 except
       to redundantly specify the `asyncio` event loop.

    """
    _EPOLLIN = ...
    _EPOLLPRI = ...
    _EPOLLOUT = ...
    _EPOLLERR = ...
    _EPOLLHUP = ...
    _EPOLLRDHUP = ...
    _EPOLLONESHOT = ...
    _EPOLLET = ...
    NONE = ...
    READ = ...
    WRITE = ...
    ERROR = ...
    _current = ...
    _ioloop_for_asyncio = ...
    @classmethod
    def configure(cls, impl, **kwargs):
        ...
    
    @staticmethod
    def instance():
        """Deprecated alias for `IOLoop.current()`.

        .. versionchanged:: 5.0

           Previously, this method returned a global singleton
           `IOLoop`, in contrast with the per-thread `IOLoop` returned
           by `current()`. In nearly all cases the two were the same
           (when they differed, it was generally used from non-Tornado
           threads to communicate back to the main thread's `IOLoop`).
           This distinction is not present in `asyncio`, so in order
           to facilitate integration with that package `instance()`
           was changed to be an alias to `current()`. Applications
           using the cross-thread communications aspect of
           `instance()` should instead set their own global variable
           to point to the `IOLoop` they want to use.

        .. deprecated:: 5.0
        """
        ...
    
    def install(self):
        """Deprecated alias for `make_current()`.

        .. versionchanged:: 5.0

           Previously, this method would set this `IOLoop` as the
           global singleton used by `IOLoop.instance()`. Now that
           `instance()` is an alias for `current()`, `install()`
           is an alias for `make_current()`.

        .. deprecated:: 5.0
        """
        ...
    
    @staticmethod
    def clear_instance():
        """Deprecated alias for `clear_current()`.

        .. versionchanged:: 5.0

           Previously, this method would clear the `IOLoop` used as
           the global singleton by `IOLoop.instance()`. Now that
           `instance()` is an alias for `current()`,
           `clear_instance()` is an alias for `clear_current()`.

        .. deprecated:: 5.0

        """
        ...
    
    @staticmethod
    def current(instance=...):
        """Returns the current thread's `IOLoop`.

        If an `IOLoop` is currently running or has been marked as
        current by `make_current`, returns that instance.  If there is
        no current `IOLoop` and ``instance`` is true, creates one.

        .. versionchanged:: 4.1
           Added ``instance`` argument to control the fallback to
           `IOLoop.instance()`.
        .. versionchanged:: 5.0
           On Python 3, control of the current `IOLoop` is delegated
           to `asyncio`, with this and other methods as pass-through accessors.
           The ``instance`` argument now controls whether an `IOLoop`
           is created automatically when there is none, instead of
           whether we fall back to `IOLoop.instance()` (which is now
           an alias for this method). ``instance=False`` is deprecated,
           since even if we do not create an `IOLoop`, this method
           may initialize the asyncio loop.
        """
        ...
    
    def make_current(self):
        """Makes this the `IOLoop` for the current thread.

        An `IOLoop` automatically becomes current for its thread
        when it is started, but it is sometimes useful to call
        `make_current` explicitly before starting the `IOLoop`,
        so that code run at startup time can find the right
        instance.

        .. versionchanged:: 4.1
           An `IOLoop` created while there is no current `IOLoop`
           will automatically become current.

        .. versionchanged:: 5.0
           This method also sets the current `asyncio` event loop.
        """
        ...
    
    @staticmethod
    def clear_current():
        """Clears the `IOLoop` for the current thread.

        Intended primarily for use by test frameworks in between tests.

        .. versionchanged:: 5.0
           This method also clears the current `asyncio` event loop.
        """
        ...
    
    @classmethod
    def configurable_base(cls):
        ...
    
    @classmethod
    def configurable_default(cls):
        ...
    
    def initialize(self, make_current=...):
        ...
    
    def close(self, all_fds=...):
        """Closes the `IOLoop`, freeing any resources used.

        If ``all_fds`` is true, all file descriptors registered on the
        IOLoop will be closed (not just the ones created by the
        `IOLoop` itself).

        Many applications will only use a single `IOLoop` that runs for the
        entire lifetime of the process.  In that case closing the `IOLoop`
        is not necessary since everything will be cleaned up when the
        process exits.  `IOLoop.close` is provided mainly for scenarios
        such as unit tests, which create and destroy a large number of
        ``IOLoops``.

        An `IOLoop` must be completely stopped before it can be closed.  This
        means that `IOLoop.stop()` must be called *and* `IOLoop.start()` must
        be allowed to return before attempting to call `IOLoop.close()`.
        Therefore the call to `close` will usually appear just after
        the call to `start` rather than near the call to `stop`.

        .. versionchanged:: 3.1
           If the `IOLoop` implementation supports non-integer objects
           for "file descriptors", those objects will have their
           ``close`` method when ``all_fds`` is true.
        """
        ...
    
    def add_handler(self, fd, handler, events):
        """Registers the given handler to receive the given events for ``fd``.

        The ``fd`` argument may either be an integer file descriptor or
        a file-like object with a ``fileno()`` method (and optionally a
        ``close()`` method, which may be called when the `IOLoop` is shut
        down).

        The ``events`` argument is a bitwise or of the constants
        ``IOLoop.READ``, ``IOLoop.WRITE``, and ``IOLoop.ERROR``.

        When an event occurs, ``handler(fd, events)`` will be run.

        .. versionchanged:: 4.0
           Added the ability to pass file-like objects in addition to
           raw file descriptors.
        """
        ...
    
    def update_handler(self, fd, events):
        """Changes the events we listen for ``fd``.

        .. versionchanged:: 4.0
           Added the ability to pass file-like objects in addition to
           raw file descriptors.
        """
        ...
    
    def remove_handler(self, fd):
        """Stop listening for events on ``fd``.

        .. versionchanged:: 4.0
           Added the ability to pass file-like objects in addition to
           raw file descriptors.
        """
        ...
    
    def set_blocking_signal_threshold(self, seconds, action):
        """Sends a signal if the `IOLoop` is blocked for more than
        ``s`` seconds.

        Pass ``seconds=None`` to disable.  Requires Python 2.6 on a unixy
        platform.

        The action parameter is a Python signal handler.  Read the
        documentation for the `signal` module for more information.
        If ``action`` is None, the process will be killed if it is
        blocked for too long.

        .. deprecated:: 5.0

           Not implemented on the `asyncio` event loop. Use the environment
           variable ``PYTHONASYNCIODEBUG=1`` instead. This method will be
           removed in Tornado 6.0.
        """
        ...
    
    def set_blocking_log_threshold(self, seconds):
        """Logs a stack trace if the `IOLoop` is blocked for more than
        ``s`` seconds.

        Equivalent to ``set_blocking_signal_threshold(seconds,
        self.log_stack)``

        .. deprecated:: 5.0

           Not implemented on the `asyncio` event loop. Use the environment
           variable ``PYTHONASYNCIODEBUG=1`` instead. This method will be
           removed in Tornado 6.0.
        """
        ...
    
    def log_stack(self, signal, frame):
        """Signal handler to log the stack trace of the current thread.

        For use with `set_blocking_signal_threshold`.

        .. deprecated:: 5.1

           This method will be removed in Tornado 6.0.
        """
        ...
    
    def start(self):
        """Starts the I/O loop.

        The loop will run until one of the callbacks calls `stop()`, which
        will make the loop stop after the current event iteration completes.
        """
        ...
    
    def stop(self):
        """Stop the I/O loop.

        If the event loop is not currently running, the next call to `start()`
        will return immediately.

        Note that even after `stop` has been called, the `IOLoop` is not
        completely stopped until `IOLoop.start` has also returned.
        Some work that was scheduled before the call to `stop` may still
        be run before the `IOLoop` shuts down.
        """
        ...
    
    def run_sync(self, func, timeout=...):
        """Starts the `IOLoop`, runs the given function, and stops the loop.

        The function must return either an awaitable object or
        ``None``. If the function returns an awaitable object, the
        `IOLoop` will run until the awaitable is resolved (and
        `run_sync()` will return the awaitable's result). If it raises
        an exception, the `IOLoop` will stop and the exception will be
        re-raised to the caller.

        The keyword-only argument ``timeout`` may be used to set
        a maximum duration for the function.  If the timeout expires,
        a `tornado.util.TimeoutError` is raised.

        This method is useful to allow asynchronous calls in a
        ``main()`` function::

            async def main():
                # do stuff...

            if __name__ == '__main__':
                IOLoop.current().run_sync(main)

        .. versionchanged:: 4.3
           Returning a non-``None``, non-awaitable value is now an error.

        .. versionchanged:: 5.0
           If a timeout occurs, the ``func`` coroutine will be cancelled.

        """
        ...
    
    def time(self):
        """Returns the current time according to the `IOLoop`'s clock.

        The return value is a floating-point number relative to an
        unspecified time in the past.

        By default, the `IOLoop`'s time function is `time.time`.  However,
        it may be configured to use e.g. `time.monotonic` instead.
        Calls to `add_timeout` that pass a number instead of a
        `datetime.timedelta` should use this function to compute the
        appropriate time, so they can work no matter what time function
        is chosen.
        """
        ...
    
    def add_timeout(self, deadline, callback, *args, **kwargs):
        """Runs the ``callback`` at the time ``deadline`` from the I/O loop.

        Returns an opaque handle that may be passed to
        `remove_timeout` to cancel.

        ``deadline`` may be a number denoting a time (on the same
        scale as `IOLoop.time`, normally `time.time`), or a
        `datetime.timedelta` object for a deadline relative to the
        current time.  Since Tornado 4.0, `call_later` is a more
        convenient alternative for the relative case since it does not
        require a timedelta object.

        Note that it is not safe to call `add_timeout` from other threads.
        Instead, you must use `add_callback` to transfer control to the
        `IOLoop`'s thread, and then call `add_timeout` from there.

        Subclasses of IOLoop must implement either `add_timeout` or
        `call_at`; the default implementations of each will call
        the other.  `call_at` is usually easier to implement, but
        subclasses that wish to maintain compatibility with Tornado
        versions prior to 4.0 must use `add_timeout` instead.

        .. versionchanged:: 4.0
           Now passes through ``*args`` and ``**kwargs`` to the callback.
        """
        ...
    
    def call_later(self, delay, callback, *args, **kwargs):
        """Runs the ``callback`` after ``delay`` seconds have passed.

        Returns an opaque handle that may be passed to `remove_timeout`
        to cancel.  Note that unlike the `asyncio` method of the same
        name, the returned object does not have a ``cancel()`` method.

        See `add_timeout` for comments on thread-safety and subclassing.

        .. versionadded:: 4.0
        """
        ...
    
    def call_at(self, when, callback, *args, **kwargs):
        """Runs the ``callback`` at the absolute time designated by ``when``.

        ``when`` must be a number using the same reference point as
        `IOLoop.time`.

        Returns an opaque handle that may be passed to `remove_timeout`
        to cancel.  Note that unlike the `asyncio` method of the same
        name, the returned object does not have a ``cancel()`` method.

        See `add_timeout` for comments on thread-safety and subclassing.

        .. versionadded:: 4.0
        """
        ...
    
    def remove_timeout(self, timeout):
        """Cancels a pending timeout.

        The argument is a handle as returned by `add_timeout`.  It is
        safe to call `remove_timeout` even if the callback has already
        been run.
        """
        ...
    
    def add_callback(self, callback, *args, **kwargs):
        """Calls the given callback on the next I/O loop iteration.

        It is safe to call this method from any thread at any time,
        except from a signal handler.  Note that this is the **only**
        method in `IOLoop` that makes this thread-safety guarantee; all
        other interaction with the `IOLoop` must be done from that
        `IOLoop`'s thread.  `add_callback()` may be used to transfer
        control from other threads to the `IOLoop`'s thread.

        To add a callback from a signal handler, see
        `add_callback_from_signal`.
        """
        ...
    
    def add_callback_from_signal(self, callback, *args, **kwargs):
        """Calls the given callback on the next I/O loop iteration.

        Safe for use from a Python signal handler; should not be used
        otherwise.

        Callbacks added with this method will be run without any
        `.stack_context`, to avoid picking up the context of the function
        that was interrupted by the signal.
        """
        ...
    
    def spawn_callback(self, callback, *args, **kwargs):
        """Calls the given callback on the next IOLoop iteration.

        Unlike all other callback-related methods on IOLoop,
        ``spawn_callback`` does not associate the callback with its caller's
        ``stack_context``, so it is suitable for fire-and-forget callbacks
        that should not interfere with the caller.

        .. versionadded:: 4.0
        """
        ...
    
    def add_future(self, future, callback):
        """Schedules a callback on the ``IOLoop`` when the given
        `.Future` is finished.

        The callback is invoked with one argument, the
        `.Future`.

        This method only accepts `.Future` objects and not other
        awaitables (unlike most of Tornado where the two are
        interchangeable).
        """
        ...
    
    def run_in_executor(self, executor, func, *args):
        """Runs a function in a ``concurrent.futures.Executor``. If
        ``executor`` is ``None``, the IO loop's default executor will be used.

        Use `functools.partial` to pass keyword arguments to ``func``.

        .. versionadded:: 5.0
        """
        ...
    
    def set_default_executor(self, executor):
        """Sets the default executor to use with :meth:`run_in_executor`.

        .. versionadded:: 5.0
        """
        ...
    
    def handle_callback_exception(self, callback):
        """This method is called whenever a callback run by the `IOLoop`
        throws an exception.

        By default simply logs the exception as an error.  Subclasses
        may override this method to customize reporting of exceptions.

        The exception itself is not passed explicitly, but is available
        in `sys.exc_info`.

        .. versionchanged:: 5.0

           When the `asyncio` event loop is used (which is now the
           default on Python 3), some callback errors will be handled by
           `asyncio` instead of this method.

        .. deprecated: 5.1

           Support for this method will be removed in Tornado 6.0.
        """
        ...
    
    def split_fd(self, fd):
        """Returns an (fd, obj) pair from an ``fd`` parameter.

        We accept both raw file descriptors and file-like objects as
        input to `add_handler` and related methods.  When a file-like
        object is passed, we must retain the object itself so we can
        close it correctly when the `IOLoop` shuts down, but the
        poller interfaces favor file descriptors (they will accept
        file-like objects and call ``fileno()`` for you, but they
        always return the descriptor itself).

        This method is provided for use by `IOLoop` subclasses and should
        not generally be used by application code.

        .. versionadded:: 4.0
        """
        ...
    
    def close_fd(self, fd):
        """Utility method to close an ``fd``.

        If ``fd`` is a file-like object, we close it directly; otherwise
        we use `os.close`.

        This method is provided for use by `IOLoop` subclasses (in
        implementations of ``IOLoop.close(all_fds=True)`` and should
        not generally be used by application code.

        .. versionadded:: 4.0
        """
        ...
    


class PollIOLoop(IOLoop):
    """Base class for IOLoops built around a select-like function.

    For concrete implementations, see `tornado.platform.epoll.EPollIOLoop`
    (Linux), `tornado.platform.kqueue.KQueueIOLoop` (BSD and Mac), or
    `tornado.platform.select.SelectIOLoop` (all platforms).
    """
    def initialize(self, impl, time_func=..., **kwargs):
        ...
    
    @classmethod
    def configurable_base(cls):
        ...
    
    @classmethod
    def configurable_default(cls):
        ...
    
    def close(self, all_fds=...):
        ...
    
    def add_handler(self, fd, handler, events):
        ...
    
    def update_handler(self, fd, events):
        ...
    
    def remove_handler(self, fd):
        ...
    
    def set_blocking_signal_threshold(self, seconds, action):
        ...
    
    def start(self):
        ...
    
    def stop(self):
        ...
    
    def time(self):
        ...
    
    def call_at(self, deadline, callback, *args, **kwargs):
        ...
    
    def remove_timeout(self, timeout):
        ...
    
    def add_callback(self, callback, *args, **kwargs):
        ...
    
    def add_callback_from_signal(self, callback, *args, **kwargs):
        ...
    


class _Timeout(object):
    """An IOLoop timeout, a UNIX timestamp and a callback"""
    __slots__ = ...
    def __init__(self, deadline, callback, io_loop) -> None:
        ...
    
    def __lt__(self, other) -> bool:
        ...
    
    def __le__(self, other) -> bool:
        ...
    


class PeriodicCallback(object):
    """Schedules the given callback to be called periodically.

    The callback is called every ``callback_time`` milliseconds.
    Note that the timeout is given in milliseconds, while most other
    time-related functions in Tornado use seconds.

    If ``jitter`` is specified, each callback time will be randomly selected
    within a window of ``jitter * callback_time`` milliseconds.
    Jitter can be used to reduce alignment of events with similar periods.
    A jitter of 0.1 means allowing a 10% variation in callback time.
    The window is centered on ``callback_time`` so the total number of calls
    within a given interval should not be significantly affected by adding
    jitter.

    If the callback runs for longer than ``callback_time`` milliseconds,
    subsequent invocations will be skipped to get back on schedule.

    `start` must be called after the `PeriodicCallback` is created.

    .. versionchanged:: 5.0
       The ``io_loop`` argument (deprecated since version 4.1) has been removed.

    .. versionchanged:: 5.1
       The ``jitter`` argument is added.
    """
    def __init__(self, callback, callback_time, jitter=...) -> None:
        ...
    
    def start(self):
        """Starts the timer."""
        ...
    
    def stop(self):
        """Stops the timer."""
        ...
    
    def is_running(self):
        """Return True if this `.PeriodicCallback` has been started.

        .. versionadded:: 4.1
        """
        ...
    

