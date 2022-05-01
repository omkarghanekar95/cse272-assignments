from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json, time
from constants import doc_constants, file_identifiers
from elastic_functions import connect_elasticsearch, document_structure

def get_single_doc(lines,curr, file_length):
	single_doc = {}
	while curr < file_length:
		line = lines[curr].strip('\n')
		# print('line is',line, curr)
		identifier = line[:2]
		if identifier in file_identifiers.keys():
			
			curr_identifier = file_identifiers[identifier]
			if identifier == '.I':
				
				if curr_identifier in single_doc:
					return single_doc, curr
				single_doc[curr_identifier] = line[2:]
			else:
				curr+=1
				single_doc[curr_identifier] = lines[curr].strip('\n')
		curr+=1
	return single_doc, curr

def create_index(es, index_name, mapping):
    """
    Create an ES index.
    :param index_name: Name of the index.
    :param mapping: Mapping of the index
    """
    logging.info(f"Creating index {index_name} with the following schema:{json.dumps(mapping, indent=2)}")
    es.indices.create(index=index_name, ignore=400, body=mapping)

def store_record(es, index_name, record):
    try:
        outcome = es.index(index=index_name, body=record, id=record[doc_constants.doc_id])
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        logging.info(str(ex))

if __name__ == "__main__":

	#logging.basicConfig(level=logging.ERROR)
	logging.basicConfig(filename='searchLogs.log', filemode='w+', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	es = connect_elasticsearch()
	
	#es.indices.delete(index=doc_constants.index_name, ignore=[400, 404])
	
	# if not es.indices.exists(index=doc_constants.index_name):
	# 	create_index(es, doc_constants.index_name, document_structure())

	start_time = time.time()
	with open(doc_constants.dfile_name) as f:
		lines = f.readlines()
		curr, file_length = 0, len(lines)
		docs_read = 0
		while curr < file_length:
			document, curr = get_single_doc(lines, curr, file_length)
					
			store_record(es,doc_constants.index_name,document)
			print('storing doc with id', document["MedID"])
			docs_read +=1
			# # if docs_read > doc_constants.docs_to_be_read:
			# 	break
			if docs_read % 1000 == 0:
				print(docs_read, ' docs read')
	print('execution time is ', time.time()-start_time)
	logging.info("execution time is %s", str(time.time()-start_time))
	
	# all documents-http://localhost:9200/company/doc/_search
	# print(
	#   json.dumps(
	#    	es.indices.get_mapping(index=doc_constants.index_name),indent=1)
	# )