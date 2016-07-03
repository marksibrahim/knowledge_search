# put two documents into elastic search
curl -XPOST 'localhost:9200/my_test/article/' -d @my_wiki.json

curl -s -XPOST 'localhost:9200/my_test/article/2' -d '{
    "title": "dog",
    "body": "my dog is the best dog in teh dog world."
}'


# sample search
curl 'localhost:9200/my_test/_search?q=dog&pretty'
curl 'ec2-52-204-244-120.compute-1.amazonaws.com:9200/wiki_test_index/_search?q=AccessibleComputing&pretty'

# or in this style
echo "second style query result:"
curl 'localhost:9200/my_test/_search?pretty' -d '{  
    "query": {    
        "query_string": {      
            "query": "cat"    
            }  
        }
    }'
