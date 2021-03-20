#!/usr/bin/python3

from datetime import datetime
from elasticsearch import Elasticsearch

import logging
logger = logging.getLogger("elasticsearch")
logger.setLevel(logging.ERROR)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
es_nodes = ['172.30.5.67:9200', '172.30.5.67:9202', '172.30.5.67:9203']

# where to save the stats to
write_index_alias = "index_stats-alias"
 
es = Elasticsearch(
    es_nodes,
    #http_auth=('elastic','mypassword'),
    scheme="http",
    #port=9200,
    #verify_certs=False,
)
 
# better: api_key=(‘id’, ‘api_key’),
 
search_query_body = {
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-1d",
              "lte": "now",
              "format": "epoch_millis"
            }
          }
        }
      ]
    }
  }
}

# get all indices
for index in es.indices.get('*'):
 
  if (not index[0].isalpha()) or 'logstash-' in index:
    # skip admin indices '.some_name'
    continue
 
  indx = es.indices.stats(index=index)
 
  if "_all" in indx:
    # total size
    size_in_bytes = indx['_all']['primaries']['store']['size_in_bytes']
    # total doc size
    doc_count = indx['_all']['primaries']['indexing']['index_total']
 
    # average doc size
    if doc_count>0:
        avg_doc_size = size_in_bytes / doc_count
    else:
        avg_doc_size = 0
        continue
 
    # now get daily doc count
    count = es.count(index=index, body=search_query_body)
    query_count = count['count']
 
    # work out daily size
    daily_size = avg_doc_size * query_count
 
    output_doc = {
      '@timestamp': datetime.now(),
      "index":  index,
      "size_in_bytes": size_in_bytes,
      "doc_count": doc_count,
      "avg_doc_size": avg_doc_size,
      "query_count": query_count,
      "daily_size": daily_size,
      "tags": ["index_size"]
    }
    print(output_doc)

    # write data back to es
    res = es.index(index=write_index_alias, body=output_doc)
    print('result: ',res)