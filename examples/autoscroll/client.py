from browser import document, window
from browser.html import P

from quipclient import Client


class MyClient(Client):
    def on_object(self, obj):
        if obj['type'] == 'output':
            mesg = 'Item %(step)s: %(data)s' % obj
            p = jq('<p>').text(mesg).appendTo(output)
            if len(obj['data']) > 25:
                p.toggleClass('yellow')
            elif len(obj['data']) > 15:
                p.toggleClass('blue')
            output.scrollTop(p.offset().top - output.offset().top + output.scrollTop())
        elif obj['type'] == 'file':
            jq('#status').text('Currently processing %s' % obj['value'])
        elif obj['type'] == 'progress':
            step, total = obj['step'], obj['total']
            percent = float(step) / total * 100
            jq('#progress').text(
                'Processed %d out of %d (%d%%)' % (step, total, percent))


jq = window.jQuery
output = jq('#output')
client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
