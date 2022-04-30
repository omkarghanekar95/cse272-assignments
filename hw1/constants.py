
class query_constants:
	qfile_name = 'datafiles/query.ohsu.1-63'
	tfidf_log_file = 'results/tf_idf.txt'
	bool_log_file = 'results/bool.txt'
	#tfidf_log_file = 'datafiles/textfile.txt'
	num = 'num'
	title = 'title'
	number = 'number'
	description = 'desc'
	qstart = '<top>'
	qend = '</top>'


	file_queries = {
		'num':'query_number',
		'title':'title',
		'desc':'description'
	}




class doc_constants:
	dfile_name = 'datafiles/ohsumed.88-91'
	index_name = 'medical_records'
	doc_type = 'articles'
	docs_to_be_read = 11000
	doc_id = 'MedID'



file_identifiers = {
					'.I':'sequenceID',
					'.U':'MedID',
					'.M':'MeSH' ,
					'.T':'Title',
					'.P':'PublicationType',
					'.W':'Abstract',
					'.A':'Author',
					'.S':'Source'
				}

