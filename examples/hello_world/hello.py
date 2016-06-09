import time
from quip import WebRunner, send


objects = [
    'Hello World',
    ('Apples', 'and', 'Oranges'),
    1234.567,
    [9, 8, 7, 6],
    999,
    {'max':  100, 'min': 45, 'lat': 41.963182, 'lng': -87.684340},
]


def hello():
    for obj in objects:
        send(obj)
        time.sleep(1)


runner = WebRunner(hello)
runner.run()
