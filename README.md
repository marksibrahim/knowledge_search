# Knowledge Search
a graph-based knowledge search engine powered by Wikipedia

search here: http://knowledgesearch.us/


# Development

1. Parse the Wikipedia XML dump into article and its first link (in the main body text).

* processing is distributed using Spark DataFrames
    * DataBricks XML package is used to delineate a page: 
    https://github.com/databricks/spark-xml

2. Store Network in Neo4j
* encodes all 9 million articles (5 million articles + 4 million redirects) and the relationships among them
 
3. Run Queries on Neo4j 
* index articles by title and add page views as a property of each article 
    * query can filter resutls by page views to return the most relevant articles

Extension: Elasticsearch to enhance matching between a search term and the relevant article.  







