from pathlib2 import Path

from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler


app = None
runner = None


def init_server(runner_, port, use_plim):
    global app, runner
    settings = dict(
        debug=True,
        # autoreload=True,
    )
    app = Application([
        (r'/', IndexHandler),
        (r'/start/', StartHandler),
        (r'/stop/', StopHandler),
        (r'/status/', StatusHandler),
        (r'/(.*)', NoCacheStaticFileHandler),
    ], **settings)
    runner = runner_
    app.sockets = set()
    app.use_plim = use_plim
    app.listen(port)

    # Return the sockets so that the runner can use them.
    return app.sockets


class IndexHandler(RequestHandler):
    def get(self):
        if app.use_plim:
            self.write(render('index.html'))
        else:
            with open('index.html') as fd:
                self.write(fd.read())


class StartHandler(RequestHandler):
    def get(self):
        if not runner.running():
            print('Starting...')
            runner.start()
        self.write('ok')

class StopHandler(RequestHandler):
    def get(self):
        if runner.running():
            print('Stopping...')
            runner.stop()
        self.write('ok')


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

    def set_extra_headers(self, path):
        self.set_header('Cache-control', 'no-cache')


def render(path):
    from mako.template import Template
    import plim
    tmpl = Template(filename=path, preprocessor=plim.preprocessor)
    return tmpl.render()
