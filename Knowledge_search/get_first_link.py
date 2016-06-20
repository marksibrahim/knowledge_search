
class Article():
"""
article class used for parsing the first link 

for a list of articles: https://en.wikipedia.org/wiki/Special:AllPages
entire dump is https://dumps.wikimedia.org/enwiki/20141008/


parsing logic:
    1. article body via xml tag
    2. clean tags: <ref>, <div>
    3. clean Media wiki templates {{ }}
    5. disregard parenthesis, not embedeed in links
    6. find first link 
        * eliminating outermost false links:
            *Image, wiktionary etc.
    first level of hierachy is check whether {{}}
        proceed to ()
        then test link
        link
"""

    def __init__(self, article_xml):
        """
        article is initialized with xml text contained inside 
        <page> tags
        """
        self.article_xml = article_xml

    

