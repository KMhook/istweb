"""Search movies for "Monty Python" and output the results.

Note: You should edit APIKEY to yours or you may be banned by service!
"""

import douban.service

# Please use your own api key instead. e.g. :
#APIKEY = "23eeeb4347bdd26bfc6b7ee9a3b755dd"
APIKEY = ''
SECRET = ''

client = douban.service.DoubanService(api_key=APIKEY)
feed = client.SearchMovie("Monty Python")
for movie in feed.entry:
    print "%s: %s" % (movie.title.text, movie.GetAlternateLink().href)
