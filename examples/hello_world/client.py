import json
from browser.websocket import WebSocket
from browser import document, window
from browser.html import P
from browser.ajax import ajax


def on_open(evt):
    print('Starting...')
    request = ajax()
    request.open('GET', '/start/', True)
    request.send()


def on_message(evt):
    div = document['output']
    div <= P(evt.data)
    print(json.loads(evt.data))


ws = WebSocket('ws://' + window.location.host + '/status/')
ws.bind('open', on_open)
ws.bind('message', on_message)
