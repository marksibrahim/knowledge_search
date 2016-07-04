from elasticsearch import Elasticsearch
es = Elasticsearch()

data_path = "/Users/mark/Dropbox/Develop/Insight/knowledge_search/data/"

with open(data_path + "sample_dump.xml") as f:



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
   
