"""

find_id.py

takes in an search term and a proposed type and finds a list of possible identifiers that will map to GNBR terms


Need to know: 
- Biolinks API json format (see BiolinksAPI.py for more information)
- MESH API json format 
"""

from iris import state_types as t
from iris import IrisCommand


from iris import state_machine as sm
from iris import util as util
from iris import iris_objects

import pandas as pd
from collections import Counter
import numpy as np

from user_functions.API import gnbrAPI
from user_functions.API import BiolinksAPI
from user_functions.API import MeshAPI


class FindID(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "Find ID"

	# give an example for iris to recognize the command
	examples = ["Find ID for {entity}"]

	argument_types = {"entity":t.String("I need a name (ex. furosemide, MTX, scurvy)."),
					"type_entity":t.Select(question="""What type of entity is this""", 
							options={"gene":'gene', 'disease':'disease', "chemical":"chemical"})}


	def command(self, entity, type_entity):
		#"filter the results for terms that are found in gnbr????"
		filtered_id_info = {}

		if type_entity == 'gene': # use biolinks to get NCBIgene: 
			api_bio = BiolinksAPI.BiolinksAPI()
			result = api_bio.get_best_id(entity, num_rows=None)
			if result is not None:
				num_found, category_info, id_info = result
				for name, identifier in id_info.items():
					if gnbrAPI.gnbrAPI.exact_match(identifier):
						 filtered_id_info[name] = identifier
				text = "There were " + str(num_found) + " mentions of gene " + entity + " found in Biolinks, and " + str(len(filtered_id_info)) + " are found in GNBR (shown below)."
			else:
				text = 'No IDs were found for: ' + entity

		elif type_entity == 'disease': #check MESH
			api_mesh = MeshAPI.MeshAPI()
			result = api_mesh.query_id(entity)


			for name, identifier in result.items():
				if gnbrAPI.gnbrAPI.exact_match(identifier):
					filtered_id_info[name] = identifier
			text = "There were " + str(len(filtered_id_info)) + " mentions of disease: " + entity + " found in GNBR network."
			text.format(len(result), entity)
			
		else: # drug, try MESH and if doesn't work use CHEBI but CHEBI not working right now
			api_mesh = MeshAPI.MeshAPI()
			result = api_mesh.query_id(entity)

			
			for name, identifier in result.items():
				if gnbrAPI.gnbrAPI.exact_match(identifier):
					filtered_id_info[name] = identifier
			text = "There were " + str(len(filtered_id_info)) + " mentions of chemical: " + entity + " found in GNBR network."
			text.format(len(result), entity)
			### TODO: add in CHEBI search if above fails

		return entity, text, filtered_id_info


	def explanation(self, result):
		entity, text, id_info = result
		print(id_info)
		if len(id_info)>0:
			# id_object = iris_objects.IrisDataframe(data=[list(item) for item in id_info.items()], column_names = ["Name", "ID"] )
			id_object = []
			count = 1
			for key in id_info.keys():
				text += "\n" + str(count) + ") " + key
				id_object.append(id_info[key])
				count += 1
			self.iris.add_to_env("concept_options", id_object)
			if "variables" not in self.iris.env:
				self.iris.add_to_env("variables", ["concept_options"])
			else:
				self.iris.env["variables"].append("concept_options")    
		return text

_FindID = FindID()

class SelectID(IrisCommand):
	title = "Select ID"

	examples = ["Select ID for {entity}"]

	argument_types = {"index":t.Int("Which of these best match your search? (Type the index)")}

	def command(self, index):
		if index > 0 and index <= len(self.iris.env["concept_options"]):
			self.iris.add_to_env("concept_id", self.iris.env["concept_options"][index-1])
		return "Great, thanks!"

_SelectID = SelectID()

class ProcessConceptID(IrisCommand):
	title = "Process concept ID"

	examples = ["Process id"]

	def command(self):
		api =  gnbrAPI.gnbrAPI()
		cid = self.iris.env["concept_id"]
		concept_result = api.concept_detail(concept_id=cid)
		statement_result = api.statement(s=[cid], relations="")
		combined_result = [concept_result[0]]
		for r in statement_result:
			if 'Disease' in r.subject.type or 'Chemical' in r.object.type:
				strings = (r.object.type, r.predicate.name, r.subject.name)
				combined_result.append((r.object.type, r.predicate.name, r.subject.name))
				self.iris.add_to_env(' '.join(strings), 
					{'relation': r.predicate.name, 'type': r.object.type, 'concept': r.subject.id})
				if "variables" not in self.iris.env:
					self.iris.add_to_env("variables", [' '.join(strings)])
				else:
					self.iris.env["variables"].append(' '.join(strings)) 
			else:
				strings = (r.subject.name, r.predicate.name, r.object.type)
				combined_result.append((r.subject.name, r.predicate.name, r.object.type))
				self.iris.add_to_env(' '.join(strings), 
					{'relation': r.predicate.name, 'type': r.object.type, 'concept': r.subject.id})
				if "variables" not in self.iris.env:
					self.iris.add_to_env("variables", [' '.join(strings)])
				else:
					self.iris.env["variables"].append(' '.join(strings)) 
		return combined_result

	def explanation(self, result):
		mentions_text = """
{} ({})

I found {:,} mentions.

{}
			"""
		additionalinfo_text = """

For more info go to: 
https://www.n2t.net/{}
		"""
		concept = result[0]
		# concept_type = concept.type.replace('Entity','').strip(',')
		synonyms = Counter(concept.synonyms)
		num_mentions = sum(synonyms.values())
		most_common = synonyms.most_common(5)
		name = most_common[0][0]
		syns = ['{}: {:.0%}'.format(syn, count/num_mentions) for syn, count in most_common]
		syns = '\n'.join(syns)
		# sentence = concept.details[0].value
		pmid = concept.details[0].tag
		# result = text.format(concept.id, name, num_mentions, syns, sentence, pmid, concept.id)
		mentions_text = mentions_text.format(concept.id, name, num_mentions, syns)

		if len(result) > 1:
			# num_results = Counter(result)
			# sum_results = sum(num_results.values())
			statement_info = Counter(result[1:]).most_common() # sort by count
			statements_text = ["\nRelationships to other entities:\n"]
			for r in statement_info:
				# r[0][0] = r[0][0].replace('Entity','').strip(',')
				statement = r[0]
				subj = statement[0].replace('Entity','').strip(',').lower()
				predicate = statement[1].replace('_',' ')
				obj = statement[2].replace('Entity','').strip(',').lower()
				count = r[1]
				formatted_result = "{} {} {} {}s ".format(subj, predicate, count, obj)
				statements_text.append(formatted_result)
			statements_text = '\n'.join(statements_text)

			# text += ' '.join(key).replace('_',' ') + ": " + str(round((num_results[key]/sum_results)*100,2)) + "%\n"
			processed_result = mentions_text + statements_text + additionalinfo_text.format(concept.id)

		# add name to environment
		if self.iris.env['Workflow'] == 'treatment_sideeffects':
			if 'workflow_path' in self.iris.env:
				self.iris.env['workflow_path'].append(concept.id)
			else:
				self.iris.add_to_env('workflow_path', [concept.id])
			processed_result = [processed_result]
			processed_result.append("To explore a specific relationship, enter command 'Workflow Two'")
		return processed_result

_ProcessConceptID = ProcessConceptID()
