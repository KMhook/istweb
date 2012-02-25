import sys

# Create your views here.
from annoying.decorators import render_to
from django.template import Context
from recommendation.models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
<<<<<<< HEAD

@render_to('recommentation/index.html')
def index(request):
   books = Book.objects.all()
   reco_books = []
   for book in books:
       reco_books.append(book)
   page = request.GET.get('page')
   if not page:
      page = 1
   paginator = Paginator(reco_books, 5)
=======
try:
   from douban.service import DoubanService
   from douban.client import OAuthClient
except ImportError, e:
   print 'please install douban-python'
   sys.exit(1)

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
            feed_read = self.service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','read')
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
                self.reco.append({subject_id: (bookfeed, [fullname])})
                continue
            else:
                for tmp in self.reco:
                    if tmp.has_key(subject_id):
                        if fullname not in tmp[subject_id][1]:
                            tmp[subject_id][1].append(fullname)
                            continue


@render_to('recommentation/index.html')
def index(request):
   page = request.GET.get('page', 1)
   reco_books = DoubanBooks()
   reco_books.get_reco()
   paginator = Paginator(reco_books.reco, 5)
>>>>>>> b1c8816ac8ea98d36c60779864c3b00117e60127
   try:
      pages = paginator.page(page)
   except PageNotAnInteger:
      pages = paginator.page(1)
   except EmptyPage:
      pages = paginator.page(paginator.num_pages)
<<<<<<< HEAD
   return {'reco_book': pages.object_list, 'page': pages}

=======
   return {'books': pages.object_list, 'page': pages}
>>>>>>> b1c8816ac8ea98d36c60779864c3b00117e60127
