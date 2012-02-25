from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

import sys

# Create your views here.
from recommendation.models import Book
from contacts.models import Contact
try:
   from douban.service import DoubanService
   from douban.client import OAuthClient
except ImportError, e:
   print e
   print 'please install douban-python'
   sys.exit(0)

class DoubanBooks(object):

    def __init__(self):
        self.HOST = 'http://www.douban.com'
        self.API_KEY = "0ff1b8ce70b305ab2fd52a6b52191101"
        self.SECRET = "47c2cb706c4ec51d"
        self.reco_books = []
        self.subjects = []
        self.reco = []
        self.href = []
        self.service = DoubanService(self.API_KEY, self.SECRET)

    def get_reco(self):
        member = Contact.objects.all()
        for tmp in member:
            feed_read = self.service.GetMyCollection('/people/%s/collection'  % tmp.douban_id, 'book', 'IST','read')
            self.get_book(feed_read, tmp.fullname)
            feed_reading = self.service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','reading')
            self.get_book(feed_reading, tmp.fullname)
            feed_wish = self.service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','wish')
            self.get_book(feed_wish, tmp.fullname)      

    def get_book(self, feed, fullname):
        for entry in feed.entry:
            book_href = entry.link[1].href
            self.href.append(book_href[21:])
            subject_id = book_href[35:]
            if subject_id not in self.subjects:
                book_href = book_href[21:]
                bookfeed = self.service.GetBook(book_href)
                self.subjects.append(subject_id)
                self.reco.append((bookfeed, [fullname], subject_id))
                continue
            else:
                for tmp in self.reco:
                   if tmp[2] == subject_id:
                        if fullname not in tmp[1]:
                            tmp[1].append(fullname)
                            continue

@periodic_task(run_every=crontab(hour="*", minute="0", day_of_week="*")) 
def test():
    douban_books = DoubanBooks()
    douban_books.get_reco()
    for reco in douban_books.reco:
        bid = reco[0].link[1].href
        title = reco[0].title.text
        #author = reco[0].author
        img_url = reco[0].link[2].href
        recommender = ''
        author = ''
        for person in reco[0].author:
            author += person.name.text + ', '
        author = author[0:-2]
        for person in reco[1]:
            recommender += ' ' + person 
        print recommender
        books = Book.objects.filter(book_id = bid)
        if not books:
           book = Book(book_title = title, 
                     book_author = author,
                     book_img_url = img_url,
                     book_id = bid,
                     book_recommender = recommender)
           book.save()
        else:
           book = books[0]
           book.book_recommender = recommender
           book.book_author = author
           book.save()

