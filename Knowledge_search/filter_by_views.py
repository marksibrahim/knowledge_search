import operator
import datetime
import six
from mwviews.api import PageviewsClient


def top_articles_by_views(articles, top_x):
    """
    returns the top x of the given list of articles
        based on page views for the previous month
        output:
            [(article1, views), (article2, views)]
    """
    p = PageviewsClient()

    # create date string based on previous month
    now = datetime.datetime.now()
    previous_month = str(now.month - 1).zfill(2)
    if previous_month == "00": previous_month = "12"
    start_date = str(now.year) + previous_month + "0100"
    end_date = str(now.year) + previous_month + "2800"

    # get views
    result = p.article_views('en.wikipedia', articles, 
            granularity='monthly', start=start_date, end=end_date)
    # clean results (six is used for backwards compatibility with python 2
    result = six.next(six.itervalues(result))
    sorted_articles = sorted(result.items(), 
            key=operator.itemgetter(1), reverse=True)
    return sorted_articles[:top_x]
    





