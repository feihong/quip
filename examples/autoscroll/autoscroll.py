import itertools
import time
from random import randint

import six

from quip import WebRunner, send


def output_stuff():
    total = randint(80, 120)
    step = 1
    while True:
        send(type='file', value='%s.txt' % get_file_name())

        for i in range(randint(8, 12)):
            if step > total:
                return
            send(type='output', step=step, data=get_data())
            send(type='progress', step=step, total=total)
            time.sleep(0.5)
            step += 1
            yield


def get_file_name():
    import uuid
    return uuid.uuid4()


def get_data():
    count = randint(5, 20)
    nums = (randint(0x4e00, 0x9fff) for i in range(count))
    return ' '.join(six.unichr(i) for i in nums)


runner = WebRunner(output_stuff, is_generator=True)
runner.run()
