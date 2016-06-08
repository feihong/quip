__title__ = 'quip'
__version__ = '0.1'
__author__ = 'Feihong Hsu'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Feihong Hsu'


import os
import functools
import inspect
import threading
import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from pathlib2 import Path
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler


executor = ThreadPoolExecutor(2)


class WebRunner(object):
    def __init__(self, func):
        self.stop_event = threading.Event()
        self.future = None
        self.func = func

    def stop(self):
        self.stop_event.set()

    def done(self):
        return self.stop_event.is_set()

    def running(self):
        if self.future:
            return self.future.running()
        else:
            return False

    def run(self, port=8000):
        loop = IOLoop.current()
        init_server(self, port)
        # Open the web browser after waiting a second for the server to start up.
        loop.call_later(1.0, webbrowser.open, 'http://localhost:%s' % port)
        loop.start()

    def start(self):
        """
        Run the generator function in a separate thread.

        """
        self.stop_event.clear()
        if inspect.isgeneratorfunction(self.func):
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
            print(ex)
            send(dict(type='error', value=str(ex)))


class SendCallable:
    def __init__(self):
        self.loop = None
        self.sockets = None

    def __call__(self, obj):
        if not self.loop:
            return
        data = json.dumps(obj)
        self.loop.add_callback(self._send, data)

    def _send(self, data):
        for socket in self.sockets:
            socket.write_message(data)


send = SendCallable()


class StartHandler(RequestHandler):
    def get(self):
        app = self.application
        if not app.runner.running():
            print('Starting...')
            app.runner.start()


class StopHandler(RequestHandler):
    def get(self):
        app = self.application
        if app.runner.running():
            print('Stopping...')
            app.runner.stop()


class StatusHandler(WebSocketHandler):
    def open(self):
        self.application.sockets.add(self)

    def on_close(self):
        self.application.sockets.remove(self)


class NoCacheStaticFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        static_dir = Path.cwd()
        kwargs.update(
            path=str(static_dir.absolute()),
            default_filename='index.html',
        )
        super(NoCacheStaticFileHandler, self).__init__(*args, **kwargs)

    # def get_content(self, abspath, start=None, end=None):
    #     import ipdb; ipdb.set_trace()
    #     return super(NoCacheStaticFileHandler, self).get_content(abspath, start, end)

    def set_extra_headers(self, path):
        self.set_header('Cache-control', 'no-cache')


def init_server(runner, port):
    settings = dict(
        debug=True,
        # autoreload=True,
    )
    app = Application([
        (r'/start/', StartHandler),
        (r'/stop/', StopHandler),
        (r'/status/', StatusHandler),
        (r'/(.*)', NoCacheStaticFileHandler),
    ], **settings)
    app.runner = runner
    app.sockets = set()
    app.listen(port)

    # Let the send callable know about this loop and the app's websockets.
    send.loop = IOLoop.current()
    send.sockets = app.sockets
