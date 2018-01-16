import time
import requests
from lxml import html
from collections import Counter


def count_tags_in_url(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    all_elms = tree.cssselect('*')
    all_tags = [x.tag for x in all_elms]

    c = Counter(all_tags)

    return c

def test_task():
    time.sleep(120)
