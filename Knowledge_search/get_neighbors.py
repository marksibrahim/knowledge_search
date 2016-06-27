import datetime
import operator
import six
from py2neo import Graph, authenticate
from mwviews.api import PageviewsClient

temp_pass = "neo4j1"


class Network():
    """
    connects and queries the first link network stored in Neo4j
        returns subset of neighbors based on page views 

    run using Python 3 to avoid utf-8 errors during the views api call
    TODO: debug New York
    """

    def __init__(self, article):
        """
        authenticates connection to the graph database
        and stores article neighbors as
            parent_article (higher category)
            comprable_articles
            child_articles (details)
        """
        # connect to database
        authenticate("52.204.244.120:7474", "neo4j", temp_pass)
        self.g = Graph("http://52.204.244.120:7474/db/data/")

        self.article = article
        self.parent_article = self.get_parent_article() 
        self.comprable_articles = self.get_comprable_articles()
        self.child_articles = self.get_child_articles()

    def get_parent_article(self):
        """
        returns article's the first link 
        """
        query = "MATCH (a:Article {title:{x}})-[r:FL_TO]->(n) "
        query += "USING INDEX a:Article(title) RETURN n.title"
        result = self.g.run(query, x=self.article).evaluate()
        return result

    def get_comprable_articles(self):
        """
        returns a list of articles linking to the same parent node
        """
        query = "MATCH (n)-[r:FL_TO]->(a: Article {title: {x}}) "
        query += "USING INDEX a:Article(title) RETURN n.title "
        results_list = []
        for record in self.g.run(query, x=self.parent_article):
            results_list.append(record["n.title"])
        return self.top_articles_by_views(results_list, 3)

    def get_child_articles(self):
        """
        returns a list of child nodes 
        (detailed topics linking to the article)
        """
        query = "MATCH (n)-[r:FL_TO]->(a: Article {title: {x}}) "
        query += "USING INDEX a:Article(title) RETURN n.title "
        result = self.g.run(query, x=self.article)
        results_list = []
        for record in result:
            results_list.append(record["n.title"])
        return self.top_articles_by_views(results_list, 7)


    def top_articles_by_views(self, articles, top_x):
        """
        returns the top x of the given list of articles
            based on page views for the previous month
            output:
                [(article1, views), (article2, views)]
        """
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
        return sorted_articles[:top_x]
        





        
