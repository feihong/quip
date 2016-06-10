from browser import document, window
from browser.html import P

from quipclient import Client


class MyClient(Client):
    def on_object(self, obj):
        if isinstance(obj, dict):
            value, total = obj['value'], obj['total']
            jq('#status').text('Processed %d out of %d' % (value, total))
            percent = float(value) / total * 100
            jq('div.progress').css('width', '%d%%' % percent)
            # jq('div.progress').animate({'width': '%d%%' % percent}, 'fast')
        else:
            p = jq('<p>').text(obj).appendTo(output)
            output.scrollTop(p.offset().top - output.offset().top + output.scrollTop())


jq = window.jQuery
output = jq('#output')
client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
