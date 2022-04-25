doc_structure = {
	"mappings": {
        "properties": {
            "sequenceID": {"type": "integer"},
            "MedID": {"type": "integer"},
            "MeSH": {"type": "text"},
            "Title": {"type": "text"},
            "PublicationType": {"type": "text"},
            "Abstract": {"type": "text"},
            "Author": {"type": "text"},
            "Source": {"type": "text"}
        }
    }
}

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