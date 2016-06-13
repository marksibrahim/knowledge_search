from py2neo import Graph, Node, Relationship

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
Sample Query
>>> from py2neo import Graph
>>> g = Graph()
>>> g.run("MATCH (a) WHERE a.name={x} RETURN a.name", x="Bob").evaluate()
u'Bob'
>>>
"""
