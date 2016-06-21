import sys
from quip import WebRunner, send


def get_news(url):
    try:
        import feedparser
        feed = feedparser.parse(url)
    except ImportError:
        print('Please install feedparser to run this example')
        return

    title = feed['feed']['title']
    print(title)
    print('=' * 80)
    send(type='title', value=title)

    for entry in feed['entries']:
        print(entry['title'])
        send(type='entry', title=entry['title'], url=entry['link'])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'https://news.ycombinator.com/rss'

    runner = WebRunner(lambda: get_news(url))
    runner.run()
