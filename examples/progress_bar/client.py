import random

from browser import document, window
from browser.html import P

from quipclient import Client


COLORS = ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue',
'light-blue', 'cyan', 'teal', 'green', 'light-green', 'lime', 'yellow',
'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey', 'black']


class MyClient(Client):
    auto_dispatch = True

    def on_progress(self, obj):
        step, total = obj['step'], obj['total']
        print('%d / %d' % (step, total))
        percent = float(step) / total * 100
        jq('div.percent').text('%d%%' % percent)
        jq('div.progress').css('width', '%d%%' % percent)

    def on_data(self, obj):
        div = jq('<div>').text(obj['value']).appendTo('#output')
        color = random.choice(COLORS)
        div.addClass(color)
        if color in ('yellow', 'amber', 'lime'):
            div.addClass('black-text')
        else:
            div.addClass('white-text')


jq = window.jQuery
client = MyClient()

jq('button').on('click', client.stop)
