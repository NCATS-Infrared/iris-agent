from iris import state_types as t
from iris import IrisCommand
from SmartAPIQueries import * 

class ListCommands(IrisCommand):
    title = "COMMANDS"
    examples = ["What commands are available?",
    			"What can you do IRIS?",
    			"What commands can I run?"]
	argument_types = {}
	def commands(self):
		cmds = [ListAllTags.title, 
				SearchKnowledgeSourceTitles.title,
				SearchKnowledgeSourceFull.title]
		return 