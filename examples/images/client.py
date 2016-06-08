from browser import document
from browser.html import SPAN

from quipclient import Client


class MyClient(Client):
    def on_open(self):
        self.start()

    def on_message(self, obj):
        div = document['output']
        div <= SPAN('%s, ' % obj)


client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
