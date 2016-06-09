from browser import document, window
from browser.html import SPAN
from quipclient import Client


class MyClient(Client):
    is_first = True

    def on_object(self, obj):
        div = document['output']
        if self.is_first:
            text = str(obj)
            self.is_first = False
        else:
            text = ', %s' % obj
        div <= SPAN(text)


client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
