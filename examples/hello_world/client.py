from quipclient import Client
from browser import document
from browser.html import P


class MyClient(Client):
    def on_object(self, obj):
        div = document['output']
        div <= P(repr(obj))
        print('%s => %r' % (type(obj).__name__, obj))


client = MyClient()
