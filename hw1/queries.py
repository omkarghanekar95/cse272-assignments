from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json, time
from constants import file_identifiers, query_constants, doc_constants
from elastic_functions import connect_elasticsearch, basic_query
#document_file_name = 'ohmused_small.88-91'


def get_single_query(lines,curr, file_length):
	single_query = {}
	while curr < file_length:
		line = lines[curr].strip('\n')
		if line == query_constants.qstart:
			curr+=1
		elif line == query_constants.qend:
			break
		else:
			line_list = line.strip('<')
			temp = ''.join(line_list)
			line_list2 = temp.split('>')
			# print('line is',line_list2, curr)
			
			if line_list2[0] == query_constants.num:
				key_value = line_list2[1].split(':')
				single_query[query_constants.num]=key_value[1]

			elif line_list2[0] == query_constants.title:
				single_query[query_constants.title]=line_list2[1]
			
			elif line_list2[0]== query_constants.description:
				print('in description')
				curr+=1
				single_query[query_constants.description]=lines[curr].strip('\n')
			curr+=1
	return single_query, curr+1

def write_to_file(algorithm_name, query, results):
 	#	R101 Q0 83653 1 0.430352 tfidf-Both 
	#	R101 Q0 83858 2 0.430207 tfidf-Both 
	#	R101 Q0 83912 3 0.429673 tfidf-Both 

    with open(, 'a+') as f:
    	for i in range(len(results)):
    		file_string = query + " Q0 "+ results[i]["_id"] +" "+ str(i+1)+" "+str(results[i]["_score"])+" "+ algorithm_name +"\n"
    		f.write(file_string)
    logging.info("Writing results to file")
    
def search_query(es, query):

	qstring= query[query_constants.title]+" "+query[query_constants.description]
	body_query = basic_query(qstring)
	print(body_query)
	try:
		result = es.search(index=doc_constants.index_name, body=body_query)
		# for res in result["hits"]["hits"]:
		# 	print("doc is ",res["_source"]["MedID"]," and score is ",res["_score"])
		write_to_file('tf-idf', query["num"], results["hits"]["hits"])
	except Exception as ex:
		print('Error in querying data')
		print(str(ex))
		logging.info(str(ex))

if __name__ == "__main__":


	#logging.basicConfig(filename='searchLogs.log', filemode='w+', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	es = connect_elasticsearch()
	
	start_time = time.time()
	with open(query_constants.qfile_name) as f:
		lines = f.readlines()
		curr, file_length = 0, len(lines)
		#queries_read = 0
		while curr < file_length:
			query, curr = get_single_query(lines, curr, file_length)
			print('searching query with id', query["num"])
			
			search_query(es,query)
			curr+=1
			a+=1 
			#queries_read +=1
	print('execution time is ', time.time()-start_time)