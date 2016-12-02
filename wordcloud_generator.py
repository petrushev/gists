#!/usr/bin/python3

import sys
from functools import cmp_to_key
import locale
from pathlib import Path

from nltk.tokenize.regexp import WordPunctTokenizer
from wordcloud import WordCloud


locale.setlocale(locale.LC_ALL, 'mk_MK.UTF-8')
_locale_sort = cmp_to_key(locale.strcoll)
wpt = WordPunctTokenizer()


def load_stopwords():
    with open('stopwords', 'rb') as f:
        stopwords = f.read().decode('utf-8').strip().split(u'\n')
    stopwords = map(str.strip, stopwords)
    return set(stopwords)


def load_lemmer():
    with open('lemmer.csv', 'rb') as f:
        lemmer = f.read().decode('utf-8').strip().split(u'\n')

    return dict([line.split(u'\t') for line in lemmer])


def count(data):
    tokens = wpt.tokenize(data.lower())
    stopwords = load_stopwords()
    lemmer = load_lemmer()

    results = {}
    for token in sorted(tokens):
        if u'а' > token or token > u'џџ' or token in stopwords or len(token) < 3:
            continue

        normalized = lemmer.get(token, token).lower()
        results[normalized] = results.get(normalized, 0) + 1

    return results


def sorter(item):
    word, count = item
    return (-count, _locale_sort(word))


def get_filename(path):
    name = path.name
    if '.' in name:
        name = '.'.join(name.split('.')[:-1])
    return name


def main():
    in_path = Path(sys.argv[1])
    name = get_filename(in_path)

    with in_path.open('rb') as f:
        data = f.read().decode('utf-8')

    counts = list(count(data).items())
    counts.sort(key=sorter)

    cloud = WordCloud(width=1000, height=750, prefer_horizontal=1, max_words=400)
    img = cloud.generate_from_frequencies(counts)

    img = img.to_image()
    img.save(u'{0}.png'.format(name))

    with open(u'{0}.data'.format(name), 'wb') as f:
        for word, cnt in counts:
            line = u'{0}\t{1}\n'.format(word, cnt).encode('utf_8')
            f.write(line)

if __name__ == '__main__':
    main()
