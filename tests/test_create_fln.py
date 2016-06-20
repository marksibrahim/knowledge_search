"""
test whether the first link network is correctly parsed
"""

from Knowledge_search import get_first_link

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
    pass
