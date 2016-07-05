# Knowledge Search [d3_net](tools/logos/d3_net.jpeg)
> a graph-based knowledge search engine powered by Wikipedia

[knowledgesearch.us](http://knowledgesearch.us/)


## Connecting Every Article in a Graph

The first link in the main body text identifies a hierarchical relationship between articles: banana links to fruit, piano to musical instruments, and so on. 
 construct a directed graph connecting all 11 million English articles (6 million redirects). For those curious about the network's topology, feel free to peek at the [research](compstorylab.org/share/papers/ibrahim2016a/index.html) inspiring this project.


Example: **Piano**

Parent | Comprable | Children
--- | --- | ---
musical instruments | Music box, Violin family, Glass harmonica | Piano Music, Piano music, Grand Piano, Lily Maisky, William Merrigan Daly


### Graph Implementation

1. Download entire XML dump available here: https://dumps.wikimedia.org/enwiki/
2. Extract the first link in the main body text (get_firstlink.py)
    * distributed computation using Spark DataFrames (on an 8-node cluster)
    * DataBricks XML package is used to delineate a page: 
    https://github.com/databricks/spark-xml
3. Store graph in neo4j 
    * index articles by title and add page views as a property of each article 
        * uses bulk import, which also includes page views as an attribute for each node
        * query can filter resutls by page views to return the most relevant articles

note matching titles between available hourly page view data and the display title extracted from the XML is imperfect (see math_views.py)

## Fuzzy Title Matching

In addition to the graph, the first 2000 characters of the main body text is also indexed for fuzzy title searching.
* implemented in scala due to incompatibility issues between databricks xml package and the elastic search module.
* elastic search query weighs the title 2x compared to the body text with elasticsearches fuzzy matching

## Application

A search term is matched to the closest title based on the elasticsearch query above. It is then translated into a neo4j query using get_neighbors.py, 
which returns the parent, comparable, adn child articles in a network view.





