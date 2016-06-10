from browser import document, window
from browser.html import P

from quipclient import Client


class MyClient(Client):
    def on_object(self, obj):
        if isinstance(obj, dict):
            jq('#status').text('Processed %d out of %d' % (obj['value'], obj['total']))
        else:
            p = jq('<p>').text(obj).appendTo(output)
            output.scrollTop(p.offset().top - output.offset().top + output.scrollTop())


jq = window.jQuery
output = jq('#output')
client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
