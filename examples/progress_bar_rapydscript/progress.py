import itertools
import time
from random import randint
import six

from quip import WebRunner, send


def output_stuff():
    total = randint(60, 140)
    for step in range(1, total+1):
        send(type='progress', step=step, total=total)
        send(type='data', value=get_data())
        time.sleep(0.5)
        yield


def get_data():
    return six.unichr(randint(945, 969))


runner = WebRunner(output_stuff, is_generator=True)
runner.run()
