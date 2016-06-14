import itertools
import time
from random import randint
import six

from quip import WebRunner, send


def output_stuff():
    total = randint(60, 140)
    for step in range(1, total+1):
        sendobj(type='progress', step=step, total=total)
        time.sleep(0.5)
        yield


def sendobj(**kwargs):
    send(kwargs)


def get_data():
    return 'X'
    # import random
    # count = random.randint(5, 20)
    # nums = (random.randint(0x4e00, 0x9fff) for i in range(count))
    # return ' '.join(six.unichr(i) for i in nums)


runner = WebRunner(output_stuff, is_generator=True)
runner.run()
