from py2neo import Graph, authenticate
import os
import configs


class Network():
    """
    connects and queries the first link network stored in Neo4j
        returns subset of neighbors based on page views 
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
        authenticate(os.environ["neo4j_ip"] + ":7474", "neo4j", os.environ["neo4j_pass"])
        self.g = Graph("http://" + os.environ["neo4j_ip"]+ ":7474/db/data/")

        self.article = article
        self.parent_article = self.get_parent_article() 
        self.comprable_articles = self.get_comprable_articles()
        self.child_articles = self.get_child_articles()

    def get_parent_article(self):
        """
        returns article's the first link 
        """
        query = "MATCH (a:Article {title:{x}})-[r:FL_TO]->(n) "
        query += "USING INDEX a:Article(title) RETURN n.title "
        query += "LIMIT 1;"
        title = self.g.run(query, x=self.article).evaluate()

        query = "MATCH (a:Article {title:{x}})-[r:FL_TO]->(n) "
        query += "USING INDEX a:Article(title) RETURN n.views "
        query += "LIMIT 1;"
        views = self.g.run(query, x=self.article).evaluate()
        return (title, views)

    def get_comprable_articles(self):
        """
        returns a list of articles linking to the same parent node
        """
        query = "MATCH (n)-[r:FL_TO]->(a: Article {title: {x}}) "
        query += "USING INDEX a:Article(title) RETURN DISTINCT n "
        query += "ORDER BY n.views DESC LIMIT 3;"
        results_list = []
        for record in self.g.run(query, x=self.parent_article[0]):
            results_list.append((record[0]["title"], record[0]["views"]))
        return results_list

    def get_child_articles(self):
        """
        returns a list of child nodes 
        (detailed topics linking to the article)
        """
        query = "MATCH (n)-[r:FL_TO]->(a: Article {title: {x}}) "
        query += "USING INDEX a:Article(title) RETURN DISTINCT n "
        query += "ORDER BY n.views DESC LIMIT 5;"
        result = self.g.run(query, x=self.article)
        results_list = []
        for record in result:
            results_list.append((record[0]["title"], record[0]["views"]))
        return results_list

