import json
from browser.websocket import WebSocket
from browser import document, window
from browser.html import SPAN
from browser.ajax import ajax


def on_open(evt):
    print('Starting...')
    request = ajax()
    request.open('GET', '/start/', True)
    request.send()


def on_message(evt):
    div = document['output']
    div <= SPAN(evt.data + ', ')


def on_click(evt):
    print('Stopping...')
    request = ajax()
    request.open('GET', '/stop/', True)
    request.send()


ws = WebSocket('ws://' + window.location.host + '/status/')
ws.bind('open', on_open)
ws.bind('message', on_message)

btn = document.get(selector='button')[0]
btn.bind('click', on_click)
