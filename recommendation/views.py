import sys

# Create your views here.
from annoying.decorators import render_to
from django.template import Context
from contacts.models import Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
try:
   from douban.service import DoubanService
   from douban.client import OAuthClient
except ImportError, e:
   print e
   print 'please install douban-python'
   sys.exit(0)

HOST = 'http://www.douban.com'
API_KEY = "0ff1b8ce70b305ab2fd52a6b52191101"
SECRET = "47c2cb706c4ec51d"
reco_books = []
subjects = []
reco = []
service = DoubanService(API_KEY, SECRET)

@render_to('recommentation/index.html')
def index(request):
   get_reco()
   paginator = Paginator(reco_books, 5)
   page = request.GET.get('page')
   if not page:
      page = 1
   try:
      pages = paginator.page(page)
   except PageNotAnInteger:
      pages = paginator.page(1)
   except EmptyPage:
      pages = paginator.page(paginator.num_pages)
   return {'books': pages.object_list, 'page': pages}

def get_reco():
   member = Contact.objects.all()
   for tmp in member:
      feed_read = service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','read')
      get_book(feed_read, tmp.fullname)
      feed_reading = service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','reading')
      get_book(feed_reading, tmp.fullname)
      feed_wish = service.GetMyCollection('/people/%s/collection' % tmp.douban_id, 'book', 'IST','wish')
      get_book(feed_wish, tmp.fullname)      

def get_book(feed, fullname):
   for entry in feed.entry:
      book_href = entry.link[1].href
      subject_id = book_href[34:]
   
      """
      if book_name not in reco_names:
         reco.append(bookfeed, [])
         reco[book_name].append(bookfeed)
         reco[book_name][1].append(fullname)
      elif book_name in reco:
         reco[book_name][1].append(fullname)
      """
      if subject_id not in subjects:
         subjects.append(subject_id)
         book_href = book_href[21:]
         bookfeed = service.GetBook(book_href)
         reco_books.append(bookfeed)
