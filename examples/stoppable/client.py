from browser import document, window
from browser.html import SPAN
from quipclient import Client


class MyClient(Client):
    def on_object(self, obj):
        div = document['output']
        div <= SPAN('%d, ' % obj)


client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
