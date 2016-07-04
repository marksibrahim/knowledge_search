from elasticsearch import Elasticsearch
import os
from Knowledge_search import configs

es = Elasticsearch([os.environ["elasticsearch_node_dns"] + ":9200"])

search_term = "computer"

# search for term
    # note title^2 means words in title are weighted twice as heavily in search

res = es.search(index="wiki_index", body={"query": {
    "multi_match": {
          "fields":  [ "body_text", "title^2" ],
                 "query": search_term,
                 "fuzziness": "AUTO",
                  } } })
# show result
for hit in res['hits']['hits']:
    print hit['_score']
    print hit['_source']['title']
   
