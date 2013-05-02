from sys import argv

from werkzeug import url_quote
import requests
from lxml.html import fromstring

# using http://kat.ph
BASEINDEX = "http://kat.ph/usearch/"

def fetch_list(query):
    """Fetches search results for a `query` at an index site"""
    query_ = url_quote(query, safe='')
    base_url = BASEINDEX + query_
    url = base_url + "/?field=seeders&sorder=desc"

    doc = fromstring(requests.get(url).content)

    for tr in doc.cssselect("tr[id^=torrent_]"):
        torrentname = tr.cssselect("div.torrentname a")[1].text_content().strip()
        for a in tr.cssselect("a[href][class]"):
            if 'idownload' in a.attrib['class']:
                href = a.attrib['href'].strip()
                if href!='#':
                    href = 'http:' + href
                    break

        yield (torrentname, href,
               tr.cssselect("td.nobr")[0].text_content(),
               tr.cssselect("td.green")[0].text_content(),
               tr.cssselect("td.red")[0].text_content())

def print_list(query):
    """Print list"""
    for i, (torrentname, _, size, seeders, leechers) in enumerate(fetch_list(query)):
        print '%d\t%s\t\t | %s\t%s\t%s' % (i+1, torrentname, size, seeders, leechers)

def download_torrent(query, num):
    """Download torrent from `num` position in results"""
    num = int(num) - 1
    entry = list(fetch_list(query))[num]
    print '%d\t%s\t\t | %s\t%s\t%s' % (num+1, entry[0], entry[2], entry[3], entry[4])
    q = requests.get(entry[1])
    fname = q.url.split('/')[-1]
    with open(fname, 'w') as f:
        f.write(q.content)
    print fname, 'downloaded.'


def main():
    argv_ = argv[1:]
    if len(argv_)==1:
        return print_list(*argv_)
    if len(argv_)==2:
        return download_torrent(*argv_)

if __name__=='__main__':
    main()
