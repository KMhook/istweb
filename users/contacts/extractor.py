# encoding: utf-8
# source: http://github.com/dziegler/excerpt_extractor/tree/master

from BeautifulSoup import BeautifulSoup, Comment, SoupStrainer
import re

CONTACT_INFO_PATTERNS = {
    'fullname': (
        re.compile(u'姓名[:：]?\s*(.*)'),
        re.compile(u'全名[:：]?\s*(.*)'),
        re.compile(r'fullname[:]?\s*(.*)', re.IGNORECASE)
    ),

    'email': (
        re.compile(r'([\w\-\.]+@\w[\w\-]+\.+[\w\-]+)'),
    ),

    'phone': (
        re.compile(u'电话[:：]?\s*(\d+)'),
        re.compile(u'手机[:：]?\s*(\d+)'),
        re.compile(r'phone[:：]?\s*(\d+)', re.IGNORECASE),
        re.compile(r'mobile[:：]?\s*(\d+)', re.IGNORECASE),
    ),

    'qq': (
        re.compile(r'qq[:：]?\s*(\d+)', re.IGNORECASE),
    ),
}


def cleanSoup(soup):
    # get rid of javascript, noscript and css
    [[tree.extract() for tree in soup(elem)] for elem in ('script','noscript','style')]
    # get rid of doctype
    subtree = soup.findAll(text=re.compile("DOCTYPE"))
    [tree.extract() for tree in subtree]
    # get rid of comments
    comments = soup.findAll(text=lambda text:isinstance(text,Comment))
    [comment.extract() for comment in comments]
    return soup


def removeHeaders(soup):
    [[tree.extract() for tree in soup(elem)] for elem in ('h1','h2','h3','h4','h5','h6')]
    return soup


def html2text(content):
    soup = removeHeaders(cleanSoup(BeautifulSoup(content, parseOnlyThese=SoupStrainer('body'))))
    text = ''.join(soup.findAll(text=True))
    return text


def extract_contact_info_from_html(html):
    text = html2text(html)
    contact = {}

    for field, patterns in CONTACT_INFO_PATTERNS.iteritems():
        for pattern in patterns:
            results = pattern.findall(text)

            if len(results) > 0:
                contact[field] = results[0]
                break

    return contact


if __name__ == '__main__':
    html = open('./test.html').read()
    c = extract_contact_info_from_html(html)

    for key, value in c.iteritems():
        print('%s: %s' % (key, value))
