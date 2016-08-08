#!/usr/bin/python2
from sys import argv

from werkzeug import url_quote
from lxml.html import fromstring
from redis.client import Redis

# using http://kat.ph
BASEINDEX = "http://dxtorrent.com/usearch/"

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
    query_ = url_quote(query, safe='')
    base_url = BASEINDEX + query_
    url = base_url + "/?field=seeders&sorder=desc"

    doc = fromstring(cached_get(url))
    doc.make_links_absolute(url)

    for tr in doc.cssselect("tr[id^=torrent_]"):
        torrentname = tr.cssselect("div.torrentname a.cellMainLink")[0].text_content().strip()
        href = None
        for a in tr.cssselect("a[href]"):
            href = a.attrib['href'].strip()
            if href.startswith('magnet:'):
                break

        if href is None:
            continue

        torrentlink = tr.cssselect("a[data-download]")[0].attrib['href'].strip()

        yield (torrentname, href,
               tr.cssselect("td.nobr")[0].text_content(),
               tr.cssselect("td.green")[0].text_content(),
               tr.cssselect("td.red")[0].text_content(),
               torrentlink)

def print_list(query):
    """Print list"""
    list_ = fetch_list(query)
    for i in range(20):
        try:
            torrentname, _, size, seeders, leechers, torrentlink = next(list_)
        except StopIteration:
            break
        else:
            print '%d\t%s\t\t | %s\t%s\t%s' % (i+1, torrentname, size, seeders, leechers)

def download_torrent(query, num):
    """Download torrent from `num` position in results"""
    num = int(num) - 1
    entry = list(fetch_list(query))[num]
    print '%d\t%s\t\t | %s\t%s\t%s' % (num+1, entry[0], entry[2], entry[3], entry[4])
    print entry[5]

def main():
    argv_ = argv[1:]
    if len(argv_)==1:
        return print_list(*argv_)
    if len(argv_)==2:
        return download_torrent(*argv_)

if __name__=='__main__':
    main()
