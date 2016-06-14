"""
stores the latest page views for the month as json
"""
import datetime

from mwviews.api import PageviewsClient

# uses parallelism to for large calls
p = PageviewsClient(100)


# get current month
now = datetime.datetime.now()

date_string = str(now.year) + now.strftime('%m') + "0101"


views = p.article_views('en.wikipedia', ['Cat', 'Dog'], granularity='monthly',
        start=date_string, end=date_string)



