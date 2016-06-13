from py2neo import Graph
from py2neo import Node, Relationship

# set up authentication parameters
# authenticate("localhost:7474", "neo4j", "neo4j")

# a good guide:
    # http://py2neo.org/2.0/intro.html

graph_db = Graph()
# default connection: 
    # http://localhost:7474/db/data/

a = Node("article", title="A", views=2)
b = Node("article", title="B", views=3)
ab = Relationship(a, "PARENT", b)

graph_db.create(ab)


