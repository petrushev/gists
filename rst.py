"""Minimal wrapper for docutils (.rst to .html conversion)"""

from docutils.core import Publisher
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser
from docutils.writers.html4css1 import Writer
from docutils.io import StringInput, StringOutput

_src, _dest = StringInput(), StringOutput(encoding='utf-8')
_pub = Publisher(reader=Reader(), parser=Parser(), writer=Writer(),
                source = _src, destination=_dest)
_publish = _pub.publish

def rst2html(source):
    _src.source = source
    _publish()
    return _dest.destination

if __name__=='__main__':
    src1 = """
Hello
=====

- what's

- up""".strip()

    print rst2html(src1)
