"""
store csv data into neo4j database
"""

from py2neo import Graph, Node, Relationship

g = Graph()

load_script = """
load csv with headers from "nodes_list.csv" as row
where has(row.title)
create (:Article {row.title})
"""

# g.cypher.execute(load_script) in previous version
    # use g.run(query) in current

g.run(load_script)

