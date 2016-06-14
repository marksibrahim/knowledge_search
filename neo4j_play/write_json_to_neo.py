from py2neo import Graph, Node, Relationship

import json

results_path = "/Users/mark/Desktop/wiki_v4/"
with open(results_path + "sample_fln.json") as f:
        fln_dict = json.load(f)

# initialize graph db
g = Graph()
tx = g.begin()


# write to graph db

for article, fl in fln_dict.iteritems():
    article_node = Node("Article", title=article)
    fl_node = Node("Article", title=fl)
    relation = Relationship(article_node, "LINKS_TO", fl_node)

    tx.create(article_node)
    tx.create(fl_node)
    tx.create(relation)

tx.commit()


"""
g = Graph()
tx = g.begin()

a = Node("Person", name="Alice")
tx.create(a)
b = Node("Person", name="Bob")
ab = Relationship(a, "KNOWS", b)
tx.create(ab)

tx.commit()
g.exists(ab)
"""


"""
SAMPLE Query
MATCH (a:Article)-[:LINKS_TO]-(neighbors) 
WHERE a.title="A" RETURN a, neighbors
"""
