from datetime import datetime
from elasticsearch import Elasticsearch
import logging
from constants import doc_structure, file_identifiers



def get_single_doc(lines,curr, file_length):
	single_doc = {}
	while curr < file_length:
		line = lines[curr].strip('\n')
		# print('line is',line, curr)
		identifier = line[:2]
		if identifier in file_identifiers.keys():
			# print(file_identifiers[identifier],identifier)
			curr_identifier = file_identifiers[identifier]
			if identifier == '.I':
				# print('found next seq id',identifier)
				if curr_identifier in single_doc:
					print('returning doc' )
					return single_doc, curr
				single_doc[curr_identifier] = identifier
			else:
				curr+=1
				single_doc[curr_identifier] = lines[curr].strip('\n')
		curr+=1
	return single_doc, curr


def connect_elasticsearch():
    _es = Elasticsearch("http://localhost:9200")
    if _es.ping():
        print('Connected to elasticsearch')
        logging.info(_es.ping())
    else:
        print('Error!, unable to connect to elastic')

    return _es

def create_index(es, index_name, mapping):
    """
    Create an ES index.
    :param index_name: Name of the index.
    :param mapping: Mapping of the index
    """
    logging.info(f"Creating index {index_name} with the following schema:{json.dumps(mapping, indent=2)}")
    es.indices.create(index=index_name, ignore=400, body=mapping)

if __name__ == "__main__":
	logging.basicConfig(level=logging.ERROR)
	
	es = connect_elasticsearch()
	create_index(es,'medical_records', doc_structure)

	with open('ohmused_small.88-91') as f:
		lines = f.readlines()
		curr, file_length = 0, len(lines)
		
		while curr < file_length:
			document, curr = get_single_doc(lines, curr, file_length)
			print('document is ', document)
		

	# print(
	#   json.dumps(
	#    	es.indices.get_mapping(index="medical_records"),indent=1)
	# )