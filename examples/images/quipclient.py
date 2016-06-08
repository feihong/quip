import json
from browser.websocket import WebSocket
from browser import document, window
from browser.ajax import ajax


class Client:
    def __init__(self):
        ws = WebSocket('ws://' + window.location.host + '/status/')
        ws.bind('open', lambda e: self.on_open())
        ws.bind('close', lambda e: self.on_close())
        ws.bind('message', lambda e: self.on_message(json.loads(e.data)))

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

    def on_open(self): pass
    def on_close(self): pass
    def on_message(self, obj): pass
