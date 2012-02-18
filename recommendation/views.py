# Create your views here.
from annoying.decorators import render_to
from django.template import Context
from contacts.models import Contact
try:
   from douban.service import DoubanService
   from douban.client import OAuthClient
except ImportError:
   print 'please install douban-python'
   sys.exit(0)

HOST = 'http://www.douban.com'
API_KEY = "0ff1b8ce70b305ab2fd52a6b52191101"
SECRET = "47c2cb706c4ec51d"
reco_books = []
reco_names = []
service = DoubanService(API_KEY, SECRET)

@render_to('recommentation/index.html')
def index(request):
   get_reco()
   return {'reco': reco_books};

def get_reco():
   member = Contact.objects.all()
   for tmp in member:
      feed_read = service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','read')
      get_book(feed_read)
      feed_reading = service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','reading')
      get_book(feed_reading)
      feed_wish = service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','wish')
      get_book(feed_wish)      

def get_book(feed):
   for entry in feed.entry:
      book_href = entry.link[1].href
      book_href = book_href[21:]
      bookfeed = service.GetBook(book_href)
      book_name = bookfeed.title.text
      if book_name not in reco_names:
         reco_names.append(book_name)
         reco_books.append(bookfeed)
