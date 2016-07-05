# Knowledge Search <a href="http://knowledgesearch.us/" rel="knowledge search"><img src="https://github.com/marksibrahim/knowledge_search/blob/master/tools/logos/d3_net.png" width="80"></a>
a graph-based knowledge search engine powered by Wikipedia

[knowledgesearch.us](http://knowledgesearch.us/)

* [Connecting Every Article in a Graph](#Connecting-Articles-in-a-Graph)
   * [Graph Implementation](#Graph-Implementation)
* [Fuzzy Title Matching](#Fuzzy-Title-Matching)
* [Setup](#Setup)
* [Application](#Application)



## <a name="Connecting-Articles-in-a-Graph"></a> Connecting Articles in a Graph

The first link in the main body text identifies a hierarchical relationship between articles: *banana* links to *fruit*, *piano* to *musical instruments*, and so on. 

The search engine constructs a directed graph connecting the 11 million English articles (6 million redirects) using the first link. For those curious about the network's topology, peek at the [research](compstorylab.org/share/papers/ibrahim2016a/index.html) inspiring this project.

> Example: **Piano**

Parent | Comparable | Children
--- | --- | ---
musical instruments | Music box, Violin family, Glass harmonica | Piano Music, Piano music, Grand Piano, Lily Maisky, William Merrigan Daly


### <a name="Graph-Implementation"></a> Graph Implementation

1. Download entire XML dump available here: https://dumps.wikimedia.org/enwiki/
2. Extract the first link in the main body text (get_first_link.py)
    * distributed computation using Spark DataFrames (on an 8-node AWS cluster)
    * Databricks XML package is used to delineate a page: 
    https://github.com/databricks/spark-xml
3. <a href="https://neo4j.com/" rel="knowledge search"><img src="https://github.com/marksibrahim/knowledge_search/blob/master/tools/logos/neo4j.png" width="80"></a> Store graph in neo4j
    * index articles by title and add page views as a property of each article 
        * uses bulk import, which also includes page views as an attribute for each node
        * query can filter resutls by page views to return the most relevant articles

*note matching titles between the available hourly page view data and displayed title is imperfect (see match_views.py)*

## <a name="Fuzzy-Title-Matching"></a>Fuzzy Title Matching

In addition to the graph, the first 2000 characters of the main body text are indexed for fuzzy title searching.
* <a href="https://www.elastic.co/" rel="knowledge search"><img src="https://github.com/marksibrahim/knowledge_search/blob/master/tools/logos/elasticsearch.png" width="30"></a> powered by Elasticsearch 
* indexing is distributed using Scala  
   * note PySpark Databricks XMl package and EsSpark (connector from Spark to Elasticsearch) are not compatible
   * build jar using Maven and run Scala (see pom.xm and index_wiki.scala)
* Elasticsearch query weighs the title 2x more heavily realtive to introductory body text

> Example: 
> "paper" --> "Pulp (paper)"

*lower-case "paper" is matched to the correct Wikipedia article title*

## <a name="Setup"></a>Setup

To install dependencies:
```
pip install requirements.txt
```

For distributed computations, the program also requires Spark, Java > 7, and Scala.

Program expects configurations in **configs.py** which sets environment variables for database and spark nodes:
```python
import os

os.environ["master_node_dns"] = "ec2-xx-xx-xx.compute-1.amazonaws.com"
os.environ["elasticsearch_node_dns"] = "ec2-xx-xx-xx.compute-1.amazonaws.com"
os.environ["neo4j_pass"] = "xxxx"
os.environ["neo4j_ip"] = "xx.xxx.xx"
```

## <a name="Application"></a>Application

Flow based on search term:
* match search term to the closest title (using Elasticsearch query above)
* fetch a subset of the network (parent, comparable, and child articles) 
* filter the subgraph by page views to return only the most relevant subset 

The front-end serves this result in a directed D3 graph.







