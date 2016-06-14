from browser import document, window
from browser.html import P

from quipclient import Client


class MyClient(Client):
    def on_object(self, obj):
        if obj['type'] == 'progress':
            step, total = obj['step'], obj['total']
            print('%d / %d' % (step, total))
            percent = float(step) / total * 100
            jq('div.percent').text('%d%%' % percent)
            jq('div.progress').css('width', '%d%%' % percent)


jq = window.jQuery
# output = jq('#output')
client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
