from elasticsearch import Elasticsearch
es = Elasticsearch(['ec2-52-73-6-251.compute-1.amazonaws.com:9200'])


# search for term
    # note title^2 means words in title are weighted twice as heavily in search
search_term = "airline"

res = es.search(index="wiki_sample_index", body={"query": {
    "multi_match": {
          "fields":  [ "body_text", "title^2" ],
                 "query": search_term,
                 "fuzziness": "AUTO",
                  } } })

# show result
for hit in res['hits']['hits']:
    print hit['_score']
    print hit['_source']['title']
   
