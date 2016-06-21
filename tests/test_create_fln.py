"""
test whether the first link network is correctly parsed
"""
from Knowledge_search import get_first_link
from Knowledge_search import get_neighbors

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
        assert New_York.parent_article == "U.S. state"
        assert "Thompson M. Scoon" in New_York.child_articles
        assert "Robert Graham (fashion brand)" in New_York.child_articles
        assert "Valdez-Yukon Railroad" in New_York.comprable_articles

    def test_Banana(self):
        Banana = get_neighbors.Network("Banana")
        assert "Banana plant" in Banana.child_articles
        assert Banana.parent_article == "fruit"
        assert "Ifco tray" in Banana.comprable_articles
        
