 # -*- coding: utf-8 -*-
import datetime
import operator
import six
import urllib
from mwviews.api import PageviewsClient

articles = ['cat', 'dog', 'New York', ]
articles = [urllib.parse.quote('Park GÃ¼ell'.encode('utf-8', 'ignore'), safe='')]

top_x = 2

p = PageviewsClient(10)

# create date string based on previous month
now = datetime.datetime.now()
previous_month = str(now.month - 1).zfill(2)
if previous_month == "00": previous_month = "12"
start_date = str(now.year) + previous_month + "0100"
end_date = str(now.year) + previous_month + "2800"

# encode in ascii for compatibility with page views api 
articles = [article.encode("ascii", 'ignore') for article in articles]
# get views
result = p.article_views('en.wikipedia', articles, 
        granularity='monthly', start=start_date, end=end_date)
# clean results (six is used for backwards compatibility with python 2
result = six.next(six.itervalues(result))
sorted_articles = sorted(result.items(), 
        key=operator.itemgetter(1), reverse=True)
# print sorted_articles[:top_x]
print(sorted_articles[:top_x])
    

