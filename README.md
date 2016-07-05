# Knowledge Search <a href="http://knowledgesearch.us/" rel="knowledge search"><img src="https://github.com/marksibrahim/knowledge_search/blob/master/tools/logos/d3_net.png" width="80"></a>
a graph-based knowledge search engine powered by Wikipedia

[knowledgesearch.us](http://knowledgesearch.us/)


## Connecting Every Article in a Graph

The first link in the main body text identifies a hierarchical relationship between articles: banana links to fruit, piano to musical instruments, and so on. The search engine constructs a directed graph connecting the 11 million English articles (6 million redirects) using the first link. For those curious about the network's topology, feel free to peek at the [research](compstorylab.org/share/papers/ibrahim2016a/index.html) inspiring this project.


Example: **Piano**

Parent | Comparable | Children
--- | --- | ---
musical instruments | Music box, Violin family, Glass harmonica | Piano Music, Piano music, Grand Piano, Lily Maisky, William Merrigan Daly


### Graph Implementation

1. Download entire XML dump available here: https://dumps.wikimedia.org/enwiki/
2. Extract the first link in the main body text (get_first_link.py)
    * distributed computation using Spark DataFrames (on an 8-node cluster)
    * DataBricks XML package is used to delineate a page: 
    https://github.com/databricks/spark-xml
3. Store graph in neo4j <a href="https://neo4j.com/" rel="knowledge search"><img src="https://github.com/marksibrahim/knowledge_search/blob/master/tools/logos/neo4j.png" width="80"></a>
    * index articles by title and add page views as a property of each article 
        * uses bulk import, which also includes page views as an attribute for each node
        * query can filter resutls by page views to return the most relevant articles

note matching titles between available hourly page view data and the display title extracted from the XML is imperfect (see math_views.py)

## Fuzzy Title Matching

In addition to the graph, the first 2000 characters of the main body text is also indexed for fuzzy title searching.
* powered by elasticsearch <a href="https://www.elastic.co/" rel="knowledge search"><img src="https://github.com/marksibrahim/knowledge_search/blob/master/tools/logos/elasticsearch.png" width="30"></a>
* indexing is distributed using scala  
   * note PySpark DataBricks XMl package and elasticsearch ES are not compatible
   * build jar using maven and run scala (see pom.xm and index_wiki.scala)
* elastic search query weighs the title 2x compared to the body text with elasticsearches fuzzy matching

## Application

A search term is matched to the closest title based on the elasticsearch query above. It is then translated into a neo4j query using get_neighbors.py, which returns the parent, comparable, and child articles in a network view.





