import time
from quip import WebRunner, send


objects = [
    'guten tag', 1234.567, 999, ('apples', 'oranges'), [9, 8, 7, 6],
    {'max':  100, 'min': 45},
]


def hello():
    for obj in objects:
        send(obj)
        time.sleep(1)


runner = WebRunner(hello)
runner.run()
