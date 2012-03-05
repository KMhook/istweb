from celery.decorators import task, periodic_task
from celery.task.schedules import crontab

import sys
from recommendation.models import Book
# Create your views here.

from doubanbooks import DoubanBooks

@periodic_task(run_every=crontab(hour="*", minute="0", day_of_week="*")) 
def test():
    douban_books = DoubanBooks()
    douban_books.get_reco()

    for reco in douban_books.reco:
        tmp_book = Book()
        tmp_book.book_id = reco[0].link[1].href
        tmp_book.book_title = reco[0].title.text
        tmp_book.book_img_url = reco[0].link[2].href
        #tmp_book.book_recommender = ''
        #tmp_book.book_author = ''
        for person in reco[0].author:
            tmp_book.book_author += person.name.text + ', '
        tmp_book.book_author = tmp_book.book_author[0:-2]
        for person in reco[1]:
            tmp_book.book_recommender += ' ' + person 
        print tmp_book.book_recommender

        books = Book.objects.filter(book_id = tmp_book.book_id)
        if not books:
            tmp_book.save()
        else:
            book = books[0]
            book.book_recommender = tmp_book.book_recommender
            book.save()

