import json
from browser.websocket import WebSocket
from browser import document, window
from browser.ajax import ajax


class Client:
    auto_dispatch = False

    def __init__(self):
        ws = WebSocket('ws://' + window.location.host + '/messages/')
        ws.bind('open', self.on_open)
        ws.bind('close', self.on_close)
        ws.bind('message', self._on_message)

    def start(self):
        print('Starting...')
        request = ajax()
        request.open('GET', '/start/', True)
        request.send()

    def stop(self):
        print('Stopping...')
        request = ajax()
        request.open('GET', '/stop/', True)
        request.send()

    def on_open(self, evt):
        self.start()

    def on_close(self, evt):
        pass

    def _on_message(self, evt):
        obj = json.loads(evt.data)
        if self.auto_dispatch:
            method = getattr(self, 'on_' + obj['type'], None)
            if method is None:
                print(obj)
            else:
                method(obj)
        else:
            self.on_object(obj)

    def on_object(self, obj):
        raise NotImplementedError()
