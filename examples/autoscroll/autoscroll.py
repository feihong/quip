import itertools
import time
from quip import WebRunner, send


def output_stuff():
    total = 100
    for i in range(total):
        send(u'Item %d: %s' % (i, get_random_chars()))
        send({'type': 'status', 'value': i+1, 'total': total})
        time.sleep(0.5)
        yield


def get_random_chars():
    import random
    count = random.randint(5, 20)
    nums = (random.randint(0x4e00, 0x9fff) for i in xrange(count))
    return ' '.join(unichr(i) for i in nums)


runner = WebRunner(output_stuff, is_generator=True)
runner.run()
