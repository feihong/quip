import random

from browser import document, window
from browser.html import P

from quipclient import Client


COLORS = ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue',
'light-blue', 'cyan', 'teal', 'green', 'light-green', 'lime', 'yellow',
'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey', 'black']


class MyClient(Client):
    def on_object(self, obj):
        if obj['type'] == 'progress':
            step, total = obj['step'], obj['total']
            print('%d / %d' % (step, total))
            percent = float(step) / total * 100
            jq('div.percent').text('%d%%' % percent)
            jq('div.progress').css('width', '%d%%' % percent)
        elif obj['type'] == 'data':
            color = random.choice(COLORS)
            jq('<div>').text(obj['value']).addClass(color).appendTo('#output')


jq = window.jQuery
client = MyClient()

btn = document.get(selector='button')[0]
btn.bind('click', client.stop)
