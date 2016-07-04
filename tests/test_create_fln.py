"""
test whether the first link network is correctly parsed
"""
from Knowledge_search import get_first_link
from Knowledge_search import get_neighbors
from Knowledge_search import configs
from elasticsearch import Elasticsearch
import os


class TestParser():
    """
    tests the first link parser based on an article's xml
    """
    def test_train_page(self):
        with open("train.xml") as f:
            train_xml = f.read()
        train = get_first_link.Article(train_xml)
        assert train.first_link == "rail transport"

class TestNetwork():
    """
    tests how the first link network is created 
    based an xml dump of articles
    """
    def test_New_York_neighbors(self):
        New_York = get_neighbors.Network("New York")
        assert New_York.parent_article[0] == "U.S. state"
        child_articles = [a[0] for a in New_York.child_articles]
        assert "Michael Rockefeller" in child_articles
        assert "Cynthia Carr" in child_articles
        comprable_articles = [a[0] for a in New_York.comprable_articles]
        assert "Wisconsin" in comprable_articles

    def test_Banana(self):
        Banana = get_neighbors.Network("Banana")
        child_articles = [a[0] for a in Banana.child_articles]
        assert "Banana plant" in child_articles
        assert Banana.parent_article[0] == "fruit"

        comprable_articles = [a[0] for a in Banana.comprable_articles]
        assert "Chili powder" in comprable_articles

    def test_page_views(self):
        """
        tests whether page views are populated
            tests whether child of list of popular cities has more than 2 views
            list includes new york city, a very popular page
        """
        list_popular = get_neighbors.Network("List of United States cities by population")
        views = [float(a[1]) for a in list_popular.child_articles]
        assert sum(views) > 2

    def test_elasticsearch(self):
        """
        tests connection to elastic search database
        and ensures there are more than 1000 entries    
        """
        es = Elasticsearch([os.environ["elasticsearch_node_dns"] + ":9200"])
        result = es.search(index="wiki_index", body={"query": {"match_all": {}}})
        assert float(result['hits']['total']) > 1000










