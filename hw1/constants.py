
class query_constants:
	qfile_name = 'datafiles/query.ohsu.1-63'
	rels_file = 'datafiles/qrels.ohsu.88-91.txt'
	num = 'num'
	title = 'title'
	number = 'number'
	description = 'desc'
	qstart = '<top>'
	qend = '</top>'
	tf_idf = 'tf_idf'
	bquery = 'boolean_query'
	rank_eval = 'relevance_feedback'
	fuzzy = 'custom_fuzzy'

	tfidf_log_file = 'results/tf_idf.txt'
	bool_log_file = 'results/bool.txt'
	rank_log_file = 'results/rank.txt'
	fuzzy_log_file = 'results/fuzzy.txt'

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

