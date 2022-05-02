
from elasticsearch import Elasticsearch
import logging

def connect_elasticsearch():
    _es = Elasticsearch("http://localhost:9200")
    if _es.ping():
        print('Connected to elasticsearch')
        logging.info(_es.ping())
    else:
        print('Error!, unable to connect to elastic')

    return _es

def document_structure():
	es_doc_structure = {
		"settings": {
			"number_of_shards": 2,
		    "number_of_replicas": 2,
			"analysis": {
			    "filter": {
			        "stop_filter": {
			            "type": "stop",
			            "stopwords": ["_english_"]
			        },
			        "stemmer_filter": {
			            "type": "stemmer",
			            "name": "minimal_english"
			        }
			    },
			    "analyzer": {
			        "my_analyzer": {
			            "type": "custom",
			            "tokenizer": "standard",
			            "filter": ["lowercase", "stop_filter", "stemmer_filter"],
			            "char_filter": ["html_strip"]
			        },
			        # "wp_raw_lowercase_analyzer": {
			        #     "type": "custom",
			        #     "tokenizer": "keyword",
			        #     "filter": ["lowercase"]
			        # }
			    }
			}
		},
		"mappings": {
			"dynamic": "strict",
	        "properties": {
	            "sequenceID": {"type": "integer"},
	            "MedID": {"type": "integer"},
	            "MeSH": {"type": "text"},
	            "Title": {
	            	"type": "text",
	            	"analyzer": "my_analyzer",
	            	"term_vector": "with_positions_offsets_payloads",
	            },
	            "PublicationType": {
	            	"type": "text",
	            	"analyzer": "my_analyzer",
	            	"term_vector": "with_positions_offsets_payloads",
	            },
	            "Abstract": {
	            	"type": "text",
	            	"analyzer": "my_analyzer",
	            	"term_vector": "with_positions_offsets_payloads",
	            },
	            "Author": {"type": "text"},
	            "Source": {"type": "text"}
	        }
	    }
	}


def basic_query(qstring):
	query = {
		"from" : 0,
		"size" : 50,
	    "query": {
	    	"query_string" : {
	    		"query" : qstring,
	    		"fields": ["Title", "PublicationType", "Abstract"]
	    	}
     	}
	}
	return query

def bool_query(title, abstract):

	bquery = {
		"from" : 0,
		"size" : 50,
		"query": {
		   "bool": {
		   		"must": { 
		            "match": { 
	             		"Title": {
	             			#"boost":2,
	             			"query": title,
	             			"analyzer": "my_analyzer"
	             		}
	             	}
	            },
	            "should":{
	            	"match":{
	            		"Abstract": abstract
	            	}
	            }
		    }
		}
	}
	return bquery

def get_rank_eval_query(qid, query_string, ratings, ids):
	
	req = [{
		"id": qid,                                  
		      "request": {                                              
		          "query": { 
		          		"multi_match": { 
		          			"query": query_string, 
		          			"fields": ["Title","Abstract" ]
		          	} 
		        }
		    }, 
		      "ratings": [
		      	{"_index": "medical_records", "_id":ids[i], "rating": ratings[i]} for i in range(len(ratings))
			]
	}]
	metric = {
		"mean_reciprocal_rank": {
                "k": 50,
                "relevant_rating_threshold": 0
        }
	}
	return req,  metric