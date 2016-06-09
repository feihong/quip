__title__ = 'quip'
__version__ = '0.1.3'
__author__ = 'Feihong Hsu'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Feihong Hsu'
__all__ = ['WebRunner', 'send']

import os
import threading
import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from pathlib2 import Path

from tornado.ioloop import IOLoop

from server import init_server


executor = ThreadPoolExecutor(2)


class WebRunner(object):
    def __init__(self, func, is_generator=False, port=8000, use_plim=True):
        self.port = port
        self.use_plim = use_plim
        self.stop_event = threading.Event()
        self.future = None
        self.func = func
        self.is_generator = is_generator

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
        send.sockets = init_server(self, self.port, self.use_plim)
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
