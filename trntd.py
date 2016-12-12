#!/usr/bin/python2
from sys import argv
from itertools import islice

from werkzeug import url_quote
from lxml.html import fromstring
from redis.client import Redis

BASEINDEX = u"https://thepiratebay.org"

rcache = Redis(db=1)

def cached_get(url, expire=3600):
    key = 'trntd:' + url

    content = rcache.get(key)
    was_cached = True

    if content == '' or content is None:
        import requests

        was_cached = False
        q = requests.get(url)
        content = q.content
        new_url = q.url

        with rcache.pipeline() as p:
            p.multi()
            p.set(key, content)
            p.expire(key, expire)

            if url != new_url:
                new_key = 'trntd:' + new_url
                p.set(new_key, content)
                p.expire(new_key, expire)

            p.execute()

    return content

def fetch_list(query):
    """Fetches search results for a `query` at an index site"""
    url = u"{0}/search/{1}/0/7/0".format(BASEINDEX, query)

    doc = fromstring(cached_get(url))
    doc.make_links_absolute(url)

    for tr in doc.cssselect("table#searchResult tr"):
        href = None
        for a in tr.cssselect("a[href]"):
            href = a.attrib['href'].strip()
            if href.startswith('magnet:'):
                break

        if href is None:
            continue

        torrentname = tr.cssselect("div.detName")
        if len(torrentname) == 0:
            continue

        torrentname = torrentname[0].text_content().strip()
        size = tr.cssselect("font.detDesc")[0].text_content().split('Size')
        size.pop(0)
        size = ' '.join(size).split(',')[0].strip()

        counts = [td.text_content().strip() for td in tr.cssselect('td')[-2:]]

        yield (torrentname, href, size, counts[0], counts[1], None)

PRINT_FMT = '%-3d %-67s %11s %7s  %5s'

def print_list(query):
    """Print list"""
    query = query.decode('utf-8')
    list_ = fetch_list(query)
    for i in range(20):
        try:
            name, magnet, size, seeders, leechers, link = next(list_)
        except StopIteration:
            break
        else:
            print PRINT_FMT % (i+1, name, size, seeders, leechers)

def download_torrent(query, num):
    """Download torrent from `num` position in results"""
    num = int(num)
    query = query.decode('utf-8')
    name, magnet, size, seeders, leechers, link = next(islice(fetch_list(query), num - 1, num))
    print PRINT_FMT % (num, name, size, seeders, leechers)
    print magnet

def main():
    argv_ = argv[1:]
    if len(argv_)==1:
        return print_list(*argv_)
    if len(argv_)==2:
        return download_torrent(*argv_)

if __name__=='__main__':
    main()
