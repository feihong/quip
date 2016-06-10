import itertools
import time
from quip import WebRunner, send


def output_stuff():
    total = 100
    for i in range(total):
        send('Item: %d' % i)
        send({'type': 'status', 'value': i+1, 'total': total})
        time.sleep(0.5)
        yield


runner = WebRunner(output_stuff, is_generator=True)
runner.run()
