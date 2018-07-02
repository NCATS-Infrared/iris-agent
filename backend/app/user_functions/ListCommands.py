from iris import state_types as t
from iris import IrisCommand
from user_functions.SmartAPIQueries import *

class ListCommands(IrisCommand):
	title = "Show Commands"
	examples = ["What commands are available?"]
	def command(self):
		cmd_classes = [ListAllKnowledgeSources, ListAllTags, SearchKnowledgeSourceTitles, 
		SearchKnowledgeSourceFull]
		cmds = [i.title for i in cmd_classes]
		return cmds
	
	def explanation(self, result):
		return "Here are commands you can run:\n" + '\n'.join(result)

ListCommands = ListCommands()