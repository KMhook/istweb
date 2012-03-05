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
        book_states = ['read', 'reading', 'wish']
        for tmp_member in member:
            for tmp_states in book_states:
                feed_read = self.service.GetMyCollection('/people/%s/collection'  % tmp_member.douban_id, 'book', 'IST', tmp_states)
                self.get_book(feed_read, tmp_member.fullname)

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

