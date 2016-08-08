import requests as rq
from lxml.html import fromstring

LETTERS = 'a,b,v,g,d,dj,e,zh,z,dz,i,j,k,l,lj,m,n,nj,o,p,r,s,t,kj,u,f,h,c,ch,dzh,sh'

URL = 'http://www.pelister.org/folklore/proverbs/index.php?sort=%s'

for letter in LETTERS.split(','):
    url = URL % letter
    doc = fromstring(rq.get(url).content)

    rows = doc.cssselect('tr')
    rows.pop(0)
    for row in rows:
        td = row.cssselect('td')[0]
        content = td.text_content()
        print content.replace('\n',' ').strip().encode('utf-8')

    print '--------'

