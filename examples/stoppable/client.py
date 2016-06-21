from browser import window
from quipclient import Client


class MyClient(Client):
    def on_object(self, obj):
        jq('<span>').text('%d, ' % obj).appendTo('#output')


jq = window.jQuery
client = MyClient()
jq('button').on('click', lambda e: client.stop())
