from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json, time
from constants import file_identifiers, query_constants as qc, doc_constants as dc
from elastic_functions import connect_elasticsearch, basic_query, bool_query, get_rank_eval_query


with open(qc.rels_file) as f:
	relslines = f.readlines()

def get_single_query(lines,curr, file_length):
	single_query = {}
	while curr < file_length:
		line = lines[curr].strip('\n')
		if line == qc.qstart:
			curr+=1
		elif line == qc.qend:
			break
		else:
			line_list = line.strip('<')
			temp = ''.join(line_list)
			line_list2 = temp.split('>')
			
			if line_list2[0] == qc.num:
				key_value = line_list2[1].split(':')
				single_query[qc.num]=key_value[1]

			elif line_list2[0] == qc.title:
				single_query[qc.title]=line_list2[1]
			
			elif line_list2[0]== qc.description:
				curr+=1
				single_query[qc.description]=lines[curr].strip('\n')
			curr+=1
	return single_query, curr+1

def write_results_to_file(algorithm, query, results):
 	#	R101 Q0 83653 1 0.430352 tfidf-Both 

	if algorithm == qc.tf_idf:
 		output_file = qc.tfidf_log_file

	elif algorithm == qc.bquery:
		output_file = qc.bool_log_file
	# print(output_file)
	with open(output_file, 'a+') as f:
		for i in range(len(results)):
			file_string = query + " Q0 "+ results[i]["_id"] +" "+ str(i+1)+" "+str(results[i]["_score"])+" "+ algorithm +"\n"
			f.write(file_string)
	logging.info("Writing results to file")

def parse_rels_file(qid):
	ratings= []
	ids = []
	for line in relslines:
		#print(line[:5], type(line[:5]), type(qid), qid)
		term = line.strip('\n').split('\t')
		if term[0] == qid:
			ids.append(term[2])
			ratings.append(int(term[3]))

	return ratings,ids
			# if line[:5] == qid:

   
def rank_search (es, query):
	
	ratings,ids = parse_rels_file(query["num"])
	req, metric = get_rank_eval_query(query["num"], query[qc.title], ratings[:20], ids[:20])
	alg = qc.rank_eval
	#print(req, metric)
	result  = es.rank_eval(index=dc.index_name, requests=req, metric =metric)
	#print(result)
	hits = result["details"][query["num"]]["hits"]
	# print(len(hits),' found hits')
	# for i in range(len(hits)):
	# 	print(hits[i]["hit"]["_id"]," and score is ", hits[i]["hit"]["_score"])
	
	output_file = qc.rank_log_file
	algorithm = "relevance_feedback"
	with open(output_file, 'a+') as f:
		for i in range(len(hits)):
			file_string = query["num"] + " Q0 "+ hits[i]["hit"]["_id"] +" "+ str(i+1)+" "+str(hits[i]["hit"]["_score"])+" "+ algorithm +"\n"
			f.write(file_string)
	logging.info("Writing results to file")


def search_query(es, query, algorithm):

	if algorithm == qc.tf_idf:
		qstring= query[qc.title]+" "+query[qc.description]
		body_query = basic_query(qstring)
		alg = qc.tf_idf
	elif algorithm == qc.bquery:
		body_query = bool_query(query[qc.title], query[qc.description])
		alg = qc.bquery
	
	#print(body_query)
	try:
		result = es.search(index=dc.index_name, body=body_query, track_scores= True)
		# for res in result["hits"]["hits"]:
		# 	print("doc is ",res["_source"]["MedID"]," and score is ",res["_score"])
		write_results_to_file(alg, query["num"], result["hits"]["hits"])

	except Exception as ex:
		print('Error in querying data', str(ex))
		logging.info(str(ex))

if __name__ == "__main__":

	logging.basicConfig(filename='searchLogs.log', filemode='w+', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	es = connect_elasticsearch()
	
	start_time = time.time()
	with open(qc.qfile_name) as f:
		lines = f.readlines()
		curr, file_length = 0, len(lines)
		while curr < file_length:
			query, curr = get_single_query(lines, curr, file_length)
			print('searching query with id', query["num"])
			
			#search_query(es, query, qc.tf_idf)
			#search_query(es, query, qc.bquery)
			rank_search(es,query)
			#curr+=1
			#a+=1
		
	print('execution time is ', time.time()-start_time)