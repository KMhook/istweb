import sys

# Create your views here.
from annoying.decorators import render_to
from django.template import Context
from recommendation.models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
   try:
      pages = paginator.page(page)
   except PageNotAnInteger:
      pages = paginator.page(1)
   except EmptyPage:
      pages = paginator.page(paginator.num_pages)
   return {'reco_book': pages.object_list, 'page': pages}
