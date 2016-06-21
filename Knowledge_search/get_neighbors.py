from py2neo import Graph, authenticate

temp_pass = "neo4j1"


class Network():
    """
    connects and queries the first link network stored in Neo4j
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
        query += "LIMIT 3"
        results_list = []
        for record in self.g.run(query, x=self.parent_article):
            results_list.append(record["n.title"])
        return results_list

    def get_child_articles(self):
        """
        returns a list of child nodes 
        (detailed topics linking to the article)
        """
        query = "MATCH (n)-[r:FL_TO]->(a: Article {title: {x}}) "
        query += "USING INDEX a:Article(title) RETURN n.title "
        query += "LIMIT 7"
        result = self.g.run(query, x=self.article)
        results_list = []
        for record in result:
            results_list.append(record["n.title"])
        return results_list
        
    def get_experiment(self):
        """
        returns a list of child nodes 
        (detailed topics linking to the article)
        """
        query = "MATCH (n)-[r:FL_TO]->(a: Article {title: {x}}) "
        query += "USING INDEX a:Article(title) RETURN n.title "
        query += "LIMIT 7"
        result = self.g.run(query, x=self.article)
        results_list = []
        for record in result:
            results_list.append(record["n.title"])
        return results_list
