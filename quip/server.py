from pathlib2 import Path

from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from mako.template import Template
from mako.lookup import TemplateLookup
import plim


app = None
runner = None

here = Path(__file__).parent
template_lookup = TemplateLookup(
    directories=[str(here)], preprocessor=plim.preprocessor)


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
        (r'.*/quipclient.py', QuipClientHandler),
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


class QuipClientHandler(RequestHandler):
    def get(self):
        path = here / 'quipclient.py'
        with path.open() as fd:
            self.write(fd.read())


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
    tmpl = Template(
        filename=path, lookup=template_lookup, preprocessor=plim.preprocessor)
    return tmpl.render()
