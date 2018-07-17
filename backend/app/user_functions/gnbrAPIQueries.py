'''
Commands to perform basic queries in gnbrAPI
'''
from iris import state_types as t
from iris import IrisCommand

from iris import state_machine as sm
from iris import util as util
from iris import iris_objects
from collections import Counter
from user_functions.API import gnbrAPI
 

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
			result['Document'], 
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


class ConceptInfo(IrisCommand):
	# what iris will call the command + how it will appear in a hint
	title = "What info do you have about {concept}?"

	# give an example for iris to recognize the command
	examples = ["What info exists about {concept}?",
				"What can you tell me about {concept}?"]

	# type annotations for each command argument, to help Iris collect missing values from a user
	argument_types = {"concept_id":t.String("I need an id (ex. MESH:C561631) or a name (ex. furosemide).")}
	
	# core logic of the command
	def command(self, concept_id):
		api =  gnbrAPI.gnbrAPI()
		cid = concept_id
		# if ':' in concept_id:
		result = api.concept_detail(concept_id=cid)
		# else:
			# result = api.concept(keywords=concept_id)
		return result

	# wrap the output of a command to display to user
	# by default this will be an identity function
	# each element of the list defines a separate chat bubble
	def explanation(self, result):

		text = """
				{} ({})

				I found {:,} mentions.

				{}

				Most informative sentence:

				{} [{}]

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
		sentence = concept.details[0].value
		pmid = concept.details[0].tag
		result = text.format(concept.id, name, num_mentions, syns, sentence, pmid, concept.id)
		return [result]

_GNBR_CONCEPT = ConceptInfo()


class GetTypesRelatedToConcept(IrisCommand):
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
		return processed_result

	def explanation(self, result):
		if len(result) > 0:
			return result
		else:
			return "No results were found"


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
		result = g.statement(concept1, t=concept2)
		return result

	def explanation(self, result):
		if len(result) > 0:
			processed_result = []
			for r in result:
				processed_result.append(r.predicate.name)
			return processed_result
		else:
			return "No relationships found"


GetRelationshipBwnConcepts = GetRelationshipBwnConcepts()

class GetEvidence(IrisCommand):
	title = "What evidence supports this?"

	examples = ["What is the proof?",
				"How can we prove this?"]

	def command(self):
		g = gnbrAPI.gnbrAPI()
		statement_id = self.iris.env['concept1'] + "|" + self.iris.env['concept2']
		result = g.evidence(statement_id)
		return result

	def explanation(self, result):
		if len(result) > 0:
			processed_result = []
			for r in result:
				text = r.label + "\n" + r.id
				processed_result.append(text)
				return processed_result
		else:
			return 'No evidence found'


GetEvidence = GetEvidence()

class GetAllRelationships(IrisCommand):
	title = "What are all relationships associated with {concept}?"

	examples = ["What relationships does {concept} have?",
				"Which relationships are associated with {concept}?"]

	argument_types = {"concept_id":t.String("I need an id (ex. MESH:C561631) or a name (ex. furosemide).")}

	def command(self, concept_id):
		g = gnbrAPI.gnbrAPI()
		result = g.statement(concept_id)
		return result

	def explanation(self, result):
		if len(result) > 0:
			processed_result = []
			for r in result:
				processed_result.append(r.predicate.name)
			return processed_result
		else:
			return "No relationships found"


GetAllRelationships = GetAllRelationships()
