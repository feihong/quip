import subprocess

from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from mako.template import Template
from mako.lookup import TemplateLookup
import plim

from .compat import Path


app = None
runner = None

here = Path(__file__).parent
resources = here / 'resources'
template_lookup = TemplateLookup(
    directories=[str(resources)], preprocessor=plim.preprocessor)


def init_server(runner_, port, use_plim, static_file_dir):
    global app, runner
    settings = dict(
        debug=True,
        # autoreload=True,
    )
    app = Application([
        (r'/', IndexHandler),
        (r'/start/', StartHandler),
        (r'/stop/', StopHandler),
        (r'/messages/', MessageHandler),
        (r'.*/quipclient.py$', QuipClientHandler),
        (r'/(.*\.pyj)$', PyJHandler),
        (r'/(.*\.styl)$', StylusHandler),
        (r'/(.*)', NoCacheStaticFileHandler),
    ], **settings)
    runner = runner_
    app.sockets = set()
    app.use_plim = use_plim
    app.static_file_dir = static_file_dir
    app.listen(port)

    # Return the sockets so that the runner can use them.
    return app.sockets


class IndexHandler(RequestHandler):
    def get(self):
        index_file = app.static_file_dir / 'index.html'
        if app.use_plim:
            self.write(render(index_file))
        else:
            self.write(index_file.read_bytes())


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


class MessageHandler(WebSocketHandler):
    def open(self):
        app.sockets.add(self)

    def on_close(self):
        app.sockets.remove(self)


class PyJHandler(RequestHandler):
    def get(self, path):
        pyj_file = app.static_file_dir / path
        if pyj_file.exists():
            self.set_header('Content-Type', 'text/javascript')
            cmd = ['rapydscript', str(pyj_file), '-j', '6', '-p', str(resources)]
            js = subprocess.check_output(cmd)
            self.write(js)
        else:
            self.write('')


class StylusHandler(WebSocketHandler):
    def get(self, path):
        stylus_file = app.static_file_dir / path
        if stylus_file.exists():
            self.set_header('Content-Type', 'text/css')
            cmd = ['stylus', '-p', str(stylus_file)]
            css = subprocess.check_output(cmd)
            self.write(css)
        else:
            self.write('')


class QuipClientHandler(RequestHandler):
    def get(self):
        path = resources / 'quipclient.py'
        self.write(path.read_bytes())


class NoCacheStaticFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        kwargs['path'] = str(app.static_file_dir)
        super(NoCacheStaticFileHandler, self).__init__(*args, **kwargs)

    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-store')


def render(path):
    tmpl = Template(
        text=path.read_text(),
        lookup=template_lookup,
        preprocessor=plim.preprocessor)
    return tmpl.render()
