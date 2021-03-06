'''
Commands to perform basic queries in gnbrAPI
'''
from iris import state_types as t
from iris import IrisCommand
import random


from iris import state_machine as sm
from iris import util as util
from iris import iris_objects
from collections import Counter
from user_functions.API import gnbrAPI
import pandas as pd
from collections import Counter
import numpy as np

from user_functions.find_id import FindID, SelectID, ProcessConceptID

class LoadGNBR(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "Start the biomedical data translator"

	# give an example for iris to recognize the command
	examples = [
	"run the translator",
	"analyze data with translator",
	"explore data with biomedical data translator"
	]

	argument_types = {
	"new_user":t.Select(question="""Hi! I am the biomedical translator \
		an AI system for exploring connections between ideas in research articles.

		Are you first time user?""", 
		options={"Yes":True, 'No':False})
	}

	# core logic of the command
	def command(self, new_user):
		# Maybe add some stuff in here to "warm up". The neo4j instance.
		self.iris.add_to_env('new_user', new_user)
		result = new_user
		return result

	# wrap the output of a command to display to user
	# by default this will be an identity function
	# each element of the list defines a separate chat bubble
	def explanation(self, result):
		if result:
			text ="""Awesome!  I'm going to walk you through a \
					few commands to show you what I can do.

					Enter 'translator types' into the command line."""	
		else:
			text="""Great to have you back!"""	

		result = text
		return [result]

_GNBR = LoadGNBR()


class HelpGNBR(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "Help me out translator"

	# give an example for iris to recognize the command
	examples = [
	"Translator, please help",
	"Translator, can I get some help?",
	"Help me navigate translator",
	]	

	argument_types = {
	"topic":t.Select(question="""What can I help you with?""", 
		options={"concepts":'concept', 'relationships':'relation'})
	}

	def command(self, topic):
		if topic == 'concept':
			result = """Concepts are great!"""
		elif topic == 'relation':
			result = """Relationships are great!"""
		else:
			result = None
		return result

	def explanation(self, result):
		return [result]

_GNBR_HELP = HelpGNBR()

class TypesGNBR(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "What types of info does translator have?"

	# give an example for iris to recognize the command
	examples = [
	"What types of info does translator know about?",
	"What types of things can I look up using translator?",
	"What types of information can translator return?"
	]

	# core logic of the command
	def command(self):
		api =  gnbrAPI.gnbrAPI()
		concept_types = api.concept_types()
		self.iris.add_to_env('types', [i.to_dict() for i in concept_types])
		types, freqs = zip( *[(info.id, int(info.frequency)) for info in concept_types] )
		types = [t.replace('Entity','').strip(',') for t in types if t]
		types = [t.replace('Theme','').strip(',') for t in types if t]
		result = {t: f for t,f in zip(types,freqs)}
		return result

	# wrap the output of a command to display to user
	# by default this will be an identity function
	# each element of the list defines a separate chat bubble
	def explanation(self, result):
		text = """I have {:,} sentences from {:,} journal articles \
				describing {:,} connections between {:,} diseases, {:,} chemicals, \
				and {:,} genes."""
		formatted_text = text.format(
			result['Sentence'],
			100,# result['Document'], 
			result['Chemical|Disease'] + 
			result['Chemical|Gene'] + 
			result['Disease|Gene'] + 
			result['Gene|Gene'],
			result['Disease'], 
			result['Chemical'], 
			result['Gene']
			)
		if self.iris.env['new_user']:
			tutorial = """\n\nType 'concept help' into the command line."""
			result = formatted_text + tutorial
		return result


_GNBR_TYPES = TypesGNBR()

class ClearVariables(IrisCommand):
	title = "Clear variables"

	examples = ["Remove variables"]
	
	# core logic of the command
	def command(self):
		if "variables" in self.iris.env:
			for var_name in list(set(self.iris.env["variables"])):
				self.iris.remove_from_env(var_name)
			self.iris.remove_from_env("variables")
			return "Current variables cleared"
		else:
			return "No variables to clear"

ClearVariables = ClearVariables()

class ConceptInfo(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "Look up concept info for {concept_id}?"

	# give an example for iris to recognize the command
	examples = ["What info exists about {concept_id}?",
				"What can you tell me about {concept_id}?"]

	# type annotations for each command argument, to help Iris collect missing values from a user
	argument_types = {"concept_id": t.YesNo("Do you have the concept id (ex. MESH:C561631)?",
						yes=t.String("What is the id?"),
						no=t.String("No worries, we'll help you find that! Just type 'next'"))}
	
	# core logic of the command
	def command(self, concept_id):
		# api =  gnbrAPI.gnbrAPI()
		if concept_id != 'next':
			self.iris.add_to_env("concept_id", concept_id)
			result = ProcessConceptID()
		else:
			result = sm.DoAll([FindID(), SelectID(), ProcessConceptID()])
		# concept_result = api.concept_detail(concept_id=cid)
		# statement_result = api.statement(s=[cid], relations="")
		# combined_result = [concept_result[0]]
		# for r in statement_result:
		# 	if 'Disease' in r.subject.type or 'Chemical' in r.object.type:
		# 		strings = (r.object.type, r.predicate.name, r.subject.name)
		# 		combined_result.append((r.object.type, r.predicate.name, r.subject.name))
		# 		self.iris.add_to_env(' '.join(strings), 
		# 			{'relation': r.predicate.name, 'type': r.object.type, 'concept': r.subject.id})
		# 	else:
		# 		strings = (r.subject.name, r.predicate.name, r.object.type)
		# 		combined_result.append((r.subject.name, r.predicate.name, r.object.type))
		# 		self.iris.add_to_env(' '.join(strings), 
		# 			{'relation': r.predicate.name, 'type': r.object.type, 'concept': r.subject.id})
		# return combined_result
		return result
	# wrap the output of a command to display to user
	# by default this will be an identity function
	# each element of the list defines a separate chat bubble
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
		if 'Workflow' in self.iris.env:
			if self.iris.env['Workflow'] == 'drug_purpose' or self.iris.env['Workflow'] == "disease_treatment":
				if 'workflow_path' in self.iris.env:
					self.iris.env['workflow_path'].append(concept.id)
				else:
					self.iris.add_to_env('workflow_path', [concept.id])
				processed_result = [processed_result]
				processed_result.append("To explore a specific relationship, enter command 'Explore concept statement'")
		return processed_result

_GNBR_CONCEPT = ConceptInfo()


class GetTypesRelatedToConcept(IrisCommand):
	title = "Explore concept statement info given {type_of_relationship}?"

	examples = ["What {type_of_relationship}?"]
	argument_types = {"args": t.EnvVar(question="What is the types term?")}

	def command(self, args):
		relation_dict = {
								"regulates": "e rg",
								"positively_regulates": "v+ e+ w a+",
								"negatively_regulates": "a- e- n",
								"directly_interacts_with": "b",
								"in_pathway_with": "i",
								"in_complex_with": "h",
								"in_cell_population_with": "q",
								"causes_or_contributes_to": "u ud j g",
								"affects_risk_for": "y",
								"correlates_with": "l x",
								"is_therapeutic_target_for": "d",
								"causes": "sa",
								"treats": "t c pa te",
								"prevents": "pr",
								"has_biomarker": "md mp",
							}
		g = gnbrAPI.gnbrAPI()
		concept_id = args['concept']
		relationship = relation_dict[ args['relation'] ]
		types = args['type']
		if 'Workflow' in self.iris.env:
			if self.iris.env['Workflow'] == 'drug_purpose' or self.iris.env['Workflow'] == "disease_treatment" or self.iris.env['Workflow'] == "random_walk":
				self.iris.env['workflow_path'].append(args['relation'] + " " + args['type'])
		self.iris.add_to_env('concept_id', concept_id)
		self.iris.add_to_env('relationship', relationship)
		self.iris.add_to_env('type', types)
		if "variables" not in self.iris.env:
			self.iris.add_to_env("variables", ['relationship'])
		else:
			self.iris.env["variables"].append('relationship')
		self.iris.env["variables"].append('type') 				
		result = g.statement(s=[concept_id], relations=relationship)
		processed_result = []
		count = 0
		for r in result:
			if count >= 3:
				break
			if r.object.type == types:
				processed_result.append((r.object.name, r.object.id))
				count += 1			
				# processed_result.append(r.object.id)
				self.iris.add_to_env(r.id, r.id)
				self.iris.add_to_env(r.object.name, (r.id, r.object.id))
				if "variables" not in self.iris.env:
					self.iris.add_to_env("variables", [r.id])
					self.iris.env["variables"].append(r.object.name) 
				else:
					self.iris.env["variables"].append(r.id)
					self.iris.env["variables"].append(r.object.name) 
				if 'Workflow' in self.iris.env:
					if self.iris.env['Workflow'] == "random_walk":
						if "random_objects" not in self.iris.env:
							self.iris.add_to_env("random_objects", [(r.object.name, r.object.id)])
						else:
							self.iris.env["random_objects"].append((r.object.name, r.object.id))
		return processed_result

	def explanation(self, result):
		text = """
{}: {} sentences
"""
		if len(result) > 0:
			processed_result = []
			for r in result:
				txt = '{} ({})'.format(r[0],r[1])
				processed_result.append(txt)
			processed_result.append("To save results, enter command 'Save dataset'")
			processed_result.append("To see evidence, enter command 'get evidence'")
			if 'Workflow' in self.iris.env:
				if self.iris.env['Workflow'] == "random_walk" and "random_objects" in self.iris.env:
					disease_name, disease_id = random.choice(self.iris.env["random_objects"])
					processed_result.append("Next, try 'Look up concept info' and use id '" + disease_id + "' for " + disease_name)
					self.iris.remove_from_env("random_objects")
			return processed_result
		else:
			return "No results were found"

"""
Older version do not delete yet!

	title = "Which {types} are related to {concept} by {relationship}?"

	examples = ["What {types} are related to {concept} by {relationship}?"]

	argument_types = {
						"types": t.Select(question="What is the types term?", options={
							"diseases": "Disease",
							"genes": "Gene",
							"chemicals": "Chemical",
						}),
						"concept": t.String("What is the concept term?"),
						"relationship": t.Select(question="What is the relationship?", options={
							"regulates": "e rg",
							"positively_regulates": "v+ e+ w a+",
							"negatively_regulates": "a- e- n",
							"directly_interacts_with": "b",
							"in_pathway_with": "i",
							"in_complex_with": "h",
							"in_cell_population_with": "q",
							"causes_or_contributes_to": "u ud j g",
							"affects_risk_for": "y",
							"correlates_with": "l x",
							"is_therapeutic_target_for": "d",
							"causes": "sa",
							"treats": "t c pa te",
							"prevents": "pr",
							"has_biomarker": "md mp",
						}),
					}

	def command(self, types, concept, relationship):
		g = gnbrAPI.gnbrAPI()
		result = g.statement(s=[concept], relations=relationship)
		processed_result = []
		for r in result:
			type_name = (r.object.type).replace('Entity','').strip(',')
			if type_name == types:
				processed_result.append(r.object.name)
		return processed_result[:3]

	def explanation(self, result):
		if len(result) > 0:
			return result
		else:
			return "No results were found"
"""

GetTypesRelatedToConcept = GetTypesRelatedToConcept()

class GetRelationshipBwnConcepts(IrisCommand):
	title = "What relationship exists between {concept1} and {concept2}?"

	examples = ["Is there a relationship between {concept1} and {concept2}?",
				"How are {concept1} and {concept2} related?"]

	argument_types = {
						"concept1": t.String("What is the concept1 term?"),
						"concept2": t.String("What is the concept2 term?"),
					}

	def command(self, concept1, concept2):
		g = gnbrAPI.gnbrAPI()
		result = g.statement(s=[concept1], relations="", t=[concept2])
		processed_result = []
		for r in result:
			processed_result.append(r.predicate.name)
		return processed_result

	def explanation(self, result):
		if len(result) > 0:
			return result
		else:
			return "No relationships found"


GetRelationshipBwnConcepts = GetRelationshipBwnConcepts()

class GetEvidence(IrisCommand):
	title = "Get evidence"

	examples = ["Get sentences",
				"Show proof"]

	argument_types = {"statement_id": t.EnvVar("For which concept?")}

	def command(self, statement_id):
		g = gnbrAPI.gnbrAPI()
		result = g.evidence(statement_id[0])
		return result

	def explanation(self, result):
		if len(result) > 0:
			processed_result = []
			for r in result[:3]:
				text = r.label + "\n" + r.id
				processed_result.append(text)
			if 'Workflow' in self.iris.env:
				if self.iris.env['Workflow'] == 'drug_purpose':
					processed_result.append("To explore another relationship, type in 'Explore concept statement'")
				elif self.iris.env['Workflow'] == "random_walk":
					processed_result.append("To explore another relationship, type in 'Explore concept statement'")
			return processed_result
		else:
			return 'No evidence found'


GetEvidence = GetEvidence()

class SelectWorkflow(IrisCommand):
	title = "Select {workflow}"

	examples = ["Pick {workflow}",
				"Choose {workflow}"]

	argument_types = {"workflow": t.Select(question="Which workflow would you like to select?", options={
						"Chemical/drug purpose and side effects": "drug_purpose",
						"Random walk": "random_walk",
						"Disease treatments": "disease_treatment",
					})}

	def command(self, workflow):
		self.iris.add_to_env("Workflow", workflow)
		if workflow == "drug_purpose" or workflow == "disease_treatment":
			return "Selected: " + workflow + "\n\nBegin by typing in 'Look up concept info'"
		elif workflow == "random_walk":
			diseases = {"fanconi anemia": "MESH:D005199", "thyroid disease": "MESH:D013959", "type II diabetes": "MESH:D003924",
						"hyperglycinemia": "MESH:D020158", "liver disease": "MESH:D058625", "myocarditis": "MESH:D009205",
						"multiple sclerosis": "MESH:D009103", "hepatitis B": "MESH:D006509", "eczema": "MESH:D004485"}
			disease_name = random.choice(list(diseases))
			disease_id = diseases[disease_name]
			return ["Selected: " + workflow, "Begin by typing in 'Look up concept info' and use id '" + disease_id + "' for " + disease_name]
			# + disease_id + "' to learn more about " + disease_name

SelectWorkflow = SelectWorkflow()

class SaveDataset(IrisCommand):
	title = "Save dataset"

	examples = ["Build dataset",
				"Store dataset"]

	def command(self):
		g = gnbrAPI.gnbrAPI()
		result = g.statement(s=[self.iris.env['concept_id']], relations=self.iris.env['relationship'])
		processed_result = []
		for r in result:
			if r.object.type == self.iris.env['type']:
				processed_result.append(r)
		relationships = []
		if len(processed_result) > 0:
			for r in processed_result:
				relationships.append(r.object.name)
			if 'Dataset' in self.iris.env:
				self.iris.env['Dataset'][self.iris.env['concept_id'] + " | " + r.predicate.name] = relationships
			else:
				relationships_dict = {self.iris.env['concept_id'] + " | " + r.predicate.name: relationships}
				self.iris.add_to_env("Dataset", relationships_dict)
			return "Saved"
		else:
			return "No results to save"

SaveDataset = SaveDataset()

# class GetAllRelationships(IrisCommand):
# 	title = "Workflow two type_statement {concept}?"

# 	examples = ["What relationships does {concept} have?",
# 				"Which relationships are associated with {concept}?"]

# 	argument_types = {"concept_id":t.EnvVar("About who?")}
# 	# argument_types = {"concept_id":t.String("I need an id (ex. MESH:C561631) or a name (ex. furosemide).")}

# 	def command(self, concept_id):
# 		g = gnbrAPI.gnbrAPI()
# 		result = g.statement(s=[concept_id], relations="")
# 		processed_result = []
# 		for r in result:
# 			if 'Disease' in r.subject.type or 'Chemical' in r.object.type:
# 				strings = (r.object.type, r.predicate.name, r.subject.name)
# 				processed_result.append((r.object.type, r.predicate.name, r.subject.name))
# 				self.iris.add_to_env(' '.join(strings), 
# 					{'relation': r.predicate.name, 'type': r.object.type, 'concept': r.subject.id})

# 			else:
# 				strings = (r.subject.name, r.predicate.name, r.object.type)
# 				processed_result.append((r.subject.name, r.predicate.name, r.object.type))
# 				self.iris.add_to_env(' '.join(strings), 
# 					{'relation': r.predicate.name, 'type': r.object.type, 'concept': r.subject.id})

# 			print(processed_result)
# 		return processed_result

# 	def explanation(self, result):
# 		if len(result) > 0:
# 			# num_results = Counter(result)
# 			# sum_results = sum(num_results.values())
# 			results = Counter(result).most_common() # sort by count
# 			text = ["Here's what they're saying about:\n"]
# 			for r in results:
# 				# r[0][0] = r[0][0].replace('Entity','').strip(',')
# 				statement = r[0]
# 				subj = statement[0].replace('Entity','').strip(',').lower()
# 				predicate = statement[1].replace('_',' ')
# 				obj = statement[2].replace('Entity','').strip(',').lower()
# 				count = r[1]
# 				formatted_result = "{} {} {} {}s ".format(subj, predicate, count, obj)
# 				text.append(formatted_result)
# 			text = '\n'.join(text)

# 				# text += ' '.join(key).replace('_',' ') + ": " + str(round((num_results[key]/sum_results)*100,2)) + "%\n"
# 			return text
# 		else:
# 			return "No relationships found"


# GetAllRelationships = GetAllRelationships()


class StatementInfo(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "Get info about {statement_id}"

	# give an example for iris to recognize the command
	examples = ["Get info about {statement_id}", "get info about statement"]

	# type annotations for each command argument, to help Iris collect missing values from a user
	argument_types = {"statement_id":t.String("I need an id (ex. MESH:D013575).")}
	
	# core logic of the command
	def command(self, statement_id):
		# api =  gnbrAPI.gnbrAPI()
		# if ':' in concept_id:
		#### TODO: currently returns all types of entities, need  the ability to return 
		# result = gnbrAPI.gnbrAPI.statement(s=[statement_id], relations='t y')
		if statement_id[:4].lower() == "mesh":
			statement_id = statement_id.upper()
		result = gnbrAPI.gnbrAPI.statement(s=[statement_id])
		# else:
			# result = api.concept(keywords=concept_id)
		return statement_id, result

	# wrap the output of a command to display to user
	# by default this will be an identity function
	# each element of the list defines a separate chat bubble
	def explanation(self, results):


		statement_id = results[0]
		statement_id_minus_mesh = statement_id.split(':')[-1]
		result = results[1] 
		# list of statements (dictionaries with key id (value str), object (value dict with id, name and type), predicate (value dict with id (curie) and name), subject (dictionary with id, name and type)
		# example statement
		# {'id': 'MESH:D013575|MESH:D000255|t',
		# 'object': {'id': 'MESH:D000255',
		#            'name': 'adenosinetriphosphate',
		#            'type': 'Chemical,Entity'},
		# 'predicate': {'id': 'curie', 'name': 'treats'},
		# 'subject': {'id': 'MESH:D013575',
		#             'name': 'syncopal_episode',
		#             'type': 'Entity,Disease'}}
		num_results = len(result)
		statements = []
		statements_header = ["object id", "object name", "object type", "predicate name", "subject id", "subject name", "subject type"]
		for statement in result:
			object_id = statement.object.id
			object_name = statement.object.name
			object_type = statement.object.type.replace('Entity','').strip(',')
			predicate_name = statement.id.split('|')[-1] + ':' + statement.predicate.name
			subject_id = statement.subject.id
			subject_name = statement.subject.name
			subject_type = statement.subject.type.replace('Entity','').strip(',')
			statements.append([object_id, object_name, object_type, predicate_name, subject_id, subject_name, subject_type])

		if len(statements)>0:
			statements_pd = pd.DataFrame(statements, columns=statements_header)
			statements_object = iris_objects.IrisDataframe(data=statements_pd)
			statements_name = 'statements_' + statement_id_minus_mesh
			self.iris.add_to_env(statements_name, statements_object)
			if "variables" not in self.iris.env:
				self.iris.add_to_env("variables", [statements_name])
			else:
				self.iris.env["variables"].append(statements_name)

			explanation = ['Total of ' + str(num_results) + ' results. See table: ' + statements_name + " for more info", statements_object]
		else:
			explanation = [statement_id + ' not found.']
		return explanation

_GNBR_STATEMENT = StatementInfo()


class StatementInfoList(IrisCommand):
	title = "Get all statements between {list_concept1} and {list_concept2}?"

	examples = ["How are these two lists of concepts related?"]

	argument_types = {"list_concept1":t.List("What concepts (entities) do you want to analyze? (enter identifiers separated by commas)"),
						"list_concept2":t.List("What concepts (entities) do you want to analyze? (enter identifiers separated by commas)")
					}

	def command(self, list_concept1, list_concept2):
		g = gnbrAPI.gnbrAPI()

		result_arr = []
		for concept1 in list_concept1:
			for concept2 in list_concept2:
				print(concept1, concept2)
				result = g.statement(s=[concept1], relations="", t=[concept2])
				print(result)
				if result:
					for r in result:
						# result_arr.append([concept1, concept2, r.predicate.name])
						result_arr.append([r.object.id, r.object.name, r.object.type.replace('Entity','').strip(','), r.predicate.name,
										 r.subject.id, r.subject.name, r.subject.type.replace('Entity','').strip(',')])
		return result_arr

	def explanation(self, result):

		statements_header = ["object id", "object name", "object type", "predicate name", "subject id", "subject name", "subject type"]
	
		if len(result)>0:
			prefix = str(random.randint(100000,999999))
			statements_pd = pd.DataFrame(result, columns=statements_header)
			statements_object = iris_objects.IrisDataframe(data=statements_pd)
			statements_name = 'statements_list_' + prefix
			self.iris.add_to_env(statements_name, statements_object)
			if "variables" not in self.iris.env:
				self.iris.add_to_env("variables", [statements_name])
			else:
				self.iris.env["variables"].append(statements_name)

			explanation = ['Total of ' + str(len(result)) + ' results. See table: ' + statements_name + " for more info", statements_object]
		else:
			return "No relationships found"
		return explanation
		# if len(result)> 0:
		# 	statements_pd = pd.DataFrame(result, columns=["Concept 1", "Concept 2", "Relationship"])
		# 	statements_object = iris_objects.IrisDataframe(data=statements_pd)
	 #        self.iris.add_to_env(statements_name, statements_object)
		
		# else:
		# 	return "No relationships found"


_GNBR_STATEMENT_LIST = StatementInfoList()

class StatementSimilarity(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "Get the similarity between {statement1_id} and {statement2_id} (Jaccard) "

	# give an example for iris to recognize the command
	examples = ["Get the similarity between {statement1_id} and {statement2_id}", "Jaccard", "similarity statements", "how similar are {statement1_id} and {statement2_id}"]

	# type annotations for each command argument, to help Iris collect missing values from a user
	argument_types = {"statement1_id":t.String("I need an id (ex. ncbigene:7018)"), 
					"statement2_id":t.String("I need another id (ex. ncbigene:4609)")}
	
	# core logic of the command
	def command(self, statement1_id, statement2_id):
		# api =  gnbrAPI.gnbrAPI()
		# if ':' in concept_id:
		#### TODO: currently returns all types of entities, need  the ability to return 
		# result = gnbrAPI.gnbrAPI.statement(s=[statement_id], relations='t y')
		if statement1_id[:4].lower() == "mesh":
			statement1_id = statement1_id.upper()
		if statement2_id[:4].lower() == "mesh":
			statement2_id = statement2_id.upper()

		result1 = gnbrAPI.gnbrAPI.statement(s=[statement1_id])
		result2 = gnbrAPI.gnbrAPI.statement(s=[statement2_id])
		# else:
			# result = api.concept(keywords=concept_id)
		return statement1_id, result1, statement2_id, result2

	# wrap the output of a command to display to user
	# by default this will be an identity function
	# each element of the list defines a separate chat bubble
	def explanation(self, results):

		statement1_id, result1, statement2_id, result2 = results

		# list of statements (dictionaries with key id (value str), object (value dict with id, name and type), predicate (value dict with id (curie) and name), subject (dictionary with id, name and type)
		# example statement
		# {'id': 'MESH:D013575|MESH:D000255|t',
		# 'object': {'id': 'MESH:D000255',
		#            'name': 'adenosinetriphosphate',
		#            'type': 'Chemical,Entity'},
		# 'predicate': {'id': 'curie', 'name': 'treats'},
		# 'subject': {'id': 'MESH:D013575',
		#             'name': 'syncopal_episode',
		#             'typeresult': 'Entity,Disease'}}
		statements1, statements2 = set(), set()
		for statement in result1:
			object_id = statement.object.id
			subject_id = statement.subject.id
			statements1.add(object_id)
			statements1.add(subject_id)

		for statement in result2:
			object_id = statement.object.id
			subject_id = statement.subject.id
			statements2.add(object_id)
			statements2.add(subject_id)



		# compute Jaccard similarity 
		intersection_cardinality = len(set.intersection(*[set(statements1), set(statements2)]))
		union_cardinality = len(set.union(*[set(statements1), set(statements2)]))
		if union_cardinality>0:
			jaccard_similarity = intersection_cardinality/float(union_cardinality)
		else:
			jaccard_similarity = 0
		self.iris.add_to_env("jaccard-" + statement1_id + "-" + statement2_id, jaccard_similarity)
		if "variables" not in self.iris.env:
			self.iris.add_to_env("variables", ["jaccard-" + statement1_id + "-" + statement2_id])
		else:
			self.iris.env["variables"].append("jaccard-" + statement1_id + "-" + statement2_id)
		print(statement1_id, len(statements1))
		print(statement2_id, len(statements2))
		print(intersection_cardinality, 'intersection', union_cardinality, 'union')

		text = """
The Jaccard similarity between 
{} ({:,} total neighbors) 
and 
{} ({:,} total neighbors) is: 
{:,} [intersection] / {:,} [union] = {:.3f} [Jaccard] 
		"""
		explanation = text.format(statement1_id, len(statements1), statement2_id, len(statements2), intersection_cardinality, union_cardinality, jaccard_similarity)

		return [explanation]

_GNBR_STATEMENT_SIMILARITY = StatementSimilarity()


class GetSimilarConcepts(IrisCommand):
	title = "Find things similar to {concept}?"

	examples = ["similarity {}?"]

	argument_types = {"args": t.EnvVar(question="Similar to who?")}

	def command(self, args):
		api = gnbrAPI.gnbrAPI()
		concept_id = args[1]
		statements = api.statement(s=[concept_id], relations="")
		source_concept, foafs = set(), set()
		for stmt in statements:
			friend = stmt.object.id
			source_concept.add(friend)
			faof_statement = api.statement(s=[friend], relations="")
			foafs.update(i.object.id for i in faof_statement if i.object.type == i.subject.type)
		similarities = {}
		for f in foafs:
			foaf_statement = api.statement(s=[f], relations="")
			foaf = set([i.object.id for i in foaf_statement])
			numerator = len(source_concept & foaf)
			denominator = len(source_concept | foaf)
			similarities[f] = 1.0*float(numerator)/(1.0*float(denominator))
		return similarities
		sorted_sims = sorted(similarities, key=similarities.get)

		return zip(sorted_sims[:10], similarities[sorted_sims[:10]])




	def explanation(self, result):
		return result

_GetSimilarConcepts = GetSimilarConcepts()
