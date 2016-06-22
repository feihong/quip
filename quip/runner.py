import json
import threading
import webbrowser
from concurrent.futures import ThreadPoolExecutor

from tornado.ioloop import IOLoop

from .compat import Path
from .server import init_server


executor = ThreadPoolExecutor(max_workers=1)


class WebRunner(object):
    def __init__(self, func, is_generator=False, port=8000, use_plim=True,
        static_file_dir=None):
        self.func = func
        self.is_generator = is_generator
        self.port = port
        self.use_plim = use_plim
        if static_file_dir is None:
            self.static_file_dir = Path.cwd()
        else:
            self.static_file_dir = Path(static_file_dir)

        self.stop_event = threading.Event()
        self.future = None

    def stop(self):
        self.stop_event.set()

    def done(self):
        return self.stop_event.is_set()

    def running(self):
        if self.future:
            return self.future.running()
        else:
            return False

    def run(self):
        loop = IOLoop.current()
        send.loop = loop
        send.sockets = init_server(
            self, self.port, self.use_plim, self.static_file_dir)
        # Open the web browser after waiting a second for the server to start up.
        loop.call_later(1.0, webbrowser.open, 'http://localhost:%s' % self.port)
        loop.start()

    def start(self):
        """
        Run self.func in a separate thread.

        """
        self.stop_event.clear()
        if self.is_generator:
            func = self._stoppable_run
        else:
            func = self.func
        self.future = executor.submit(func)
        self.future.add_done_callback(self._done_callback)

    def _stoppable_run(self):
        for _ in self.func():
            if self.stop_event.is_set():
                break
        self.stop_event.set()

    def _done_callback(self, future):
        # If there was an exception inside of the function sent to
        # executor.submit(), then it won't be raised until you call
        # future.result().
        try:
            future.result()
        except Exception as ex:
            import traceback
            traceback.print_exc()
            send(type='error', value=str(ex))


class SendCallable:
    """
    A callable object that is used to communicate with the browser.

    """

    def __init__(self):
        self.loop = None
        self.sockets = None

    def __call__(self, obj=None, **kwargs):
        """
        It is safe to call this method from outside the main thread that is
        running the Tornado event loop.

        """
        if not self.loop:
            return
        if obj is not None:
            data = json.dumps(obj)
            if kwargs:
                print('Warning: Keyword arguments to send() are ignored when '
                      'single positional argument is given')
        else:
            data = json.dumps(kwargs)
        self.loop.add_callback(self._send, data)

    def _send(self, data):
        "Write the given data to all connected websockets."
        for socket in self.sockets:
            socket.write_message(data)


send = SendCallable()
