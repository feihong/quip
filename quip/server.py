from pathlib2 import Path

from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler


app = None
runner = None


def init_server(runner_, port):
    global app, runner
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
    runner = runner_
    app.sockets = set()
    app.listen(port)

    # Return the sockets so that the runner can use them.
    return app.sockets


class StartHandler(RequestHandler):
    def get(self):
        if not runner.running():
            print('Starting...')
            runner.start()


class StopHandler(RequestHandler):
    def get(self):
        if runner.running():
            print('Stopping...')
            runner.stop()


class StatusHandler(WebSocketHandler):
    def open(self):
        app.sockets.add(self)

    def on_close(self):
        app.sockets.remove(self)


class NoCacheStaticFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        static_dir = Path.cwd()
        kwargs.update(
            path=str(static_dir.absolute()),
            default_filename='index.html',
        )
        super(NoCacheStaticFileHandler, self).__init__(*args, **kwargs)

    # @classmethod
    # def get_content(cls, abspath, start=None, end=None):
    #     print(type(abspath))
    #     return super(NoCacheStaticFileHandler, cls).get_content(abspath, start, end)

    def set_extra_headers(self, path):
        self.set_header('Cache-control', 'no-cache')
