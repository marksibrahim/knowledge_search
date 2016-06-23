from datetime import datetime
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

# load sample wiki json
with open("sample_wiki.json") as f:
    sample_wiki = json.load(f)


res = es.index(index="test-index", doc_type='article', id=1, body=sample_wiki)

res = es.get(index="test-index", doc_type='article', id=1)
print(res['_source'])


es.search(index="test-index"
"""
es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
"""
