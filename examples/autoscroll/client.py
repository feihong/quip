from browser import window

from quipclient import Client


class MyClient(Client):
    auto_dispatch = True

    def on_output(self, obj):
        output = jq('#output')
        mesg = 'Item %(step)s: %(data)s' % obj
        p = jq('<p>').text(mesg).appendTo(output)
        if len(obj['data']) > 25:
            p.toggleClass('yellow')
        elif len(obj['data']) > 15:
            p.toggleClass('blue')

        # Make output scroll to the bottom.
        output.scrollTop(p.offset().top - output.offset().top + output.scrollTop())

    def on_file(self, obj):
        (jq('#status')
            .text('Currently processing %s' % obj['value'])
            .effect('highlight', 1000))

    def on_progress(self, obj):
        step, total = obj['step'], obj['total']
        percent = float(step) / total * 100
        jq('#progress').text(
            'Processed %d out of %d (%d%%)' % (step, total, percent))


jq = window.jQuery
client = MyClient()

jq('button').on('click', lambda e: client.stop())
