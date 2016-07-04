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
    def test_light_neighbors(self):
        piano = get_neighbors.Network("light")
        assert piano.parent_article[0] == "electromagnetic radiation"

        child_articles = [a[0] for a in piano.child_articles]
        assert "Light Wave" in child_articles
        assert "Visible Light" in child_articles

        comprable_articles = [a[0] for a in piano.comprable_articles]
        assert "Sunlight" in comprable_articles

    def test_piano_neighbors(self):
        piano = get_neighbors.Network("Piano")
        assert piano.parent_article[0] == "musical instrument"

        child_articles = [a[0] for a in piano.child_articles]
        assert "Grand Piano" in child_articles

        comprable_articles = [a[0] for a in piano.comprable_articles]
        assert "Violin family" in comprable_articles

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

    def test_fuzzy_title_matching(self):
        """
        tests whether a generic term is matched to a title
        """
        # lower-case computer should be matched to Computers
        assert get_neighbors.Network("computer").article == "Computers"

        











