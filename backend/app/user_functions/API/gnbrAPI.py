from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

"""
This module uses a swagger generated client library (i.e. swagger_slient).  
For package installation instructions check out the readme at 
https://github.com/NCATS-Infrared/gnbr-client-python
"""

class gnbarAPI():

	@staticmethod
	def concept_detail(concept_id):
		"""
		# concept_id # str | a [CURIE-encoded](https://www.w3.org/TR/curie/) identifier to the beacon. Unknown CURIES should simply be ignored (silent match failure). 
		"""
		api_instance = swagger_client.ConceptsApi()
		try:
			api_response = api_instance.get_concept_details(concept_id)
			pprint(api_response)
		except ApiException as e:
			print("Exception when calling ConceptsApi->get_concept_details: %s\n" % e)

	@staticmethod
	def concept(keywords=None, types=None, page_number = 56, page_size = 56):
		"""
		# keywords = 'Furosemide' # str | a (urlencoded) space delimited set of keywords or substrings against which to match concept names and synonyms
		# types = 'types_example' # str | a (url-encoded) space-delimited set of semantic groups (specified as codes gene, pathway, etc.) to which to constrain concepts matched by the main keyword search (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)  (optional)
		# page_number = 56 # int | (1-based) number of the page to be returned in a paged set of query results  (optional)
		# page_size = 56 # int | number of concepts per page to be returned in a paged set of query results  (optional)
		"""
		if not types: 
			types = 'Entity'
		# create an instance of the API class
		api_instance = swagger_client.ConceptsApi()
		try:
		    api_response = api_instance.get_concepts(keywords, types=types, page_number=page_number, page_size=page_size)
		    pprint(api_response)
		except ApiException as e:
		    print("Exception when calling ConceptsApi->get_concepts: %s\n" % e)

	@staticmethod
	def statement(s, relations=None, t=None, keywords=None, types=None, page_number = 56, page_size = 56):
		"""
		# s # list[str] | a set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of  'source' concepts possibly known to the beacon. Unknown CURIES should simply be ignored (silent match failure). 
		# relations # str | a (url-encoded, space-delimited) string of predicate relation identifiers with which to constrain the statement relations retrieved  for the given query seed concept. The predicate ids sent should  be as published by the beacon-aggregator by the /predicates API endpoint.  (optional)
		# t # list[str] | (optional) an array set of [CURIE-encoded](https://www.w3.org/TR/curie/)  identifiers of 'target' concepts possibly known to the beacon.  Unknown CURIEs should simply be ignored (silent match failure).  (optional)
		# keywords # str | a (url-encoded, space-delimited) string of keywords or substrings against which to match the subject, predicate or object names of the set of concept-relations matched by any of the input exact matching concepts  (optional)
		# types # str | a (url-encoded, space-delimited) string of concept types (specified as codes gene, pathway, etc.) to which to constrain the subject or object concepts associated with the query seed concept (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)  (optional)
		# page_number # int | (1-based) number of the page to be returned in a paged set of query results  (optional)
		# page_size # int | number of concepts per page to be returned in a paged set of query results  (optional)
		"""
		if not t:
			t = []
		# create an instance of the API class
		api_instance = swagger_client.StatementsApi()
		try:
		    api_response = api_instance.get_statements(s, relations=relations, t=t, keywords=keywords, types=types, page_number=page_number, page_size=page_size)
		    pprint(api_response)
		except ApiException as e:
		    print("Exception when calling StatementsApi->get_statements: %s\n" % e)

	@staticmethod
	def evidence(statement_id, keywords, page_number = 56, page_size = 56):
		"""
		# statement_id = 'statement_id_example' # str | (url-encoded) CURIE identifier of the concept-relationship statement (\"assertion\", \"claim\") for which associated evidence is sought 
		# keywords = 'keywords_example' # str | (url-encoded, space delimited) keyword filter to apply against the label field of the annotation  (optional)
		# page_number = 56 # int | (1-based) number of the page to be returned in a paged set of query results  (optional)
		# page_size = 56 # int | number of cited references per page to be returned in a paged set of query results  (optional)
		"""
		# create an instance of the API class
		api_instance = swagger_client.StatementsApi()
		try:
		    api_response = api_instance.get_evidence(statement_id, keywords=keywords, page_number=page_number, page_size=page_size)
		    pprint(api_response)
		except ApiException as e:
		    print("Exception when calling StatementsApi->get_evidence: %s\n" % e)

if __name__ == '__main__':

####	Evidence Test
	start = time.time()
	gnbarAPI.evidence(statement_id='MESH:D013575|ncbigene:6331|t', keywords=None)
	end = time.time()
	print(end - start)

####	# Statement Test
	start = time.time()
	gnbarAPI.statement(s=['MESH:D013575'], relations='t', t=[])
	end = time.time()
	print(end - start)



####	Concept Test
	start = time.time()
	gnbarAPI.concept(keywords='syncope',types='Disease' )
	end = time.time()
	print(end - start)

####	Concept Detail Test
	start = time.time()
	gnbarAPI.concept_detail('MESH:D005355')
	end = time.time()
	print(end - start)

