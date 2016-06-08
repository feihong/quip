import itertools
import time
from quip import WebRunner, send


def keep_going_forever():
    for i in itertools.count():
        send(i)
        time.sleep(1)
        yield


runner = WebRunner(keep_going_forever)
runner.run(use_plim=True)
