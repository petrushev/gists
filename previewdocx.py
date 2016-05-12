"""
docx to txt `convertor`
----------------------
Usage
python2 previewdocx.py < mydoc.docx

"""

from zipfile import ZipFile
from sys import stdin
from StringIO import StringIO

from lxml.html import fromstring, HtmlElement


def preview(docx_content):
    docx_file = StringIO(docx_content)

    zip_ = ZipFile(docx_file)
    doc_file = zip_.open('word/document.xml')
    doc = fromstring(doc_file.read())

    elements = tuple(doc.iter())
    for el in elements:
        p = HtmlElement('p')
        p.text = '\n'
        el.append(p)

    text = doc.text_content()
    while ' \n' in text:
        text = text.replace(' \n', '\n')
    while '\n\n' in text:
        text = text.replace('\n\n', '\n')
    text = text.strip()

    return text

docx_content = stdin.read()
text = preview(docx_content)
print text.encode('utf-8')
