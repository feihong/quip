import itertools
import time
from quip import WebRunner, send_obj


def keep_going_forever():
    for i in itertools.count():
        send_obj(i)
        time.sleep(1)
        yield


runner = WebRunner(keep_going_forever, is_generator=True)
runner.run()
