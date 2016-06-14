# Knowledge Search
a graph-based knowledge search engine powered by Wikipedia


# Development

## Build Network 
Goal: process xml dump into a hash table

* benchmark stream process
    * 54 hours to process entire XML (see benchmark_streamking.ipynb)
* distribute computation via HDFS and Spark
    * 2.5 hours on 8 node cluster 

## Get Page Views 
* aggregate daily page view dumps into a single csv


## Store in Graph Database

* neo4j encodes relationship among articles and associates a number of page views with each








