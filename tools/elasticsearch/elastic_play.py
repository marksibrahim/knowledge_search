from datetime import datetime
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

doc1 = {
    'title': 'Banana',
    'body_text': 'A banana is a fruit of the botanical family banana',
}

doc2 = {
    'title': 'Orange',
    'body_text': 'An Orange is a fruit of the botanical family similar to banana',
}

doc3 = {
    'title': 'Train',
    'body_text': 'A train is a form of rail transport',
}

docs = [doc1, doc2, doc3]

# index documents
for i, doc in enumerate(docs):
    es.index(index="my_index", doc_type='article', id=i, body=doc)

# search for term
    # note title^2 means words in title are weighted twice as heavily in search
search_term = "banana"

res = es.search(index="my_index", body={"query": {
    "multi_match": {
          "fields":  [ "body_text", "title^2" ],
                 "query": search_term,
                 "fuzziness": "AUTO",
                  } } })

# show result
for hit in res['hits']['hits']:
    print hit['_source']
