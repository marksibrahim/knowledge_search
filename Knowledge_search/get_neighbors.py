from py2neo import Graph, authenticate
from elasticsearch import Elasticsearch
import os
import configs



class Network():
    """
    connects and queries the first link network stored in Neo4j
        returns subset of neighbors based on page views 
    """

    def __init__(self, search_term):
        """
        authenticates connection to the graph database
        and stores article neighbors as
            parent_article (higher category)
            comprable_articles
            child_articles (details)
        """
        # connect to databases: neo4j and elasticsearch
        authenticate(os.environ["neo4j_ip"] + ":7474", "neo4j", os.environ["neo4j_pass"])
        self.g = Graph("http://" + os.environ["neo4j_ip"]+ ":7474/db/data/")
        self.es = Elasticsearch([os.environ["elasticsearch_node_dns"] + ":9200"])


        self.search_term = search_term
        self.article = self.fuzzy_match_title()
        self.parent_article = self.get_parent_article() 
        self.comprable_articles = self.get_comprable_articles()
        self.child_articles = self.get_child_articles()

    def fuzzy_match_title(self):
        """
        returns the title of the Wikipedia article most closely matching
        the search term
            based on title and first 2k characters of body text
            title is weighed 2x in search 
        """
        result = self.es.search(index="wiki_index", body={"query": {
                "multi_match": {
                  "fields":  [ "body_text", "title^2" ],
                         "query": self.search_term,
                         "fuzziness": "AUTO",
                          } } })
        best_match = result['hits']['hits'][0]['_source']['title']
        # if title contains a comma, return the next best match
        if "," not in best_match:
            return best_match
        for hit in result['hits']['hits'][1:]:
            if "," not in hit['_source']['title']:
                return hit['_source']['title']
         
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

    def build_json_nodes_views(self):
        """
        returns a list of dictionaries with the nodes 
        and views in d3_plus format:
            [{"title": "cat", "views": 2}, ..]
        """
        nodes = []
        nodes.append({"title": self.parent_article[0], "views": self.parent_article[1],
            "relationship": "parent"})
        for node in self.child_articles:
            node_views = {"title": node[0], "views": node[1], "relationship": "child"}
            if node_views not in nodes:
                nodes.append(node_views)
        for node in self.comprable_articles:
            node_views = {"title": node[0], "views": node[1], "relationship": "similar"}
            if node_views not in nodes:
                nodes.append(node_views)
        return nodes

    def build_json_node_connections(self):
        """
        returns a list of dictionaries with the nodes 
        and their connections in d3_plus format:
            [{"source": "cat", "target": "dog"}, ...]
        """
        connections = []
        connections.append({"source": self.article, "target": self.parent_article[0]})
        for node in self.child_articles:
            connection = {"source": node[0], "target": self.article}
            if connection not in connections:
                connections.append(connection)
        for node in self.comprable_articles:
            connection = {"source": node[0], "target":self.parent_article[0]}
            if connection not in connections:
                connections.append(connection)
        return connections
        
