from iris import state_types as t
from iris import IrisCommand
# from user_functions.SmartAPIQueries import ListAllTags

class ListCommands(IrisCommand):
	title = "Show Commands"
	examples = ["What commands are available?"]
	def commands(self):
		# cmds = []
		return "hey"
	
	def explanation(self, result):
		return ["Here are commands you can run ", str(result)]

ListCommands = ListCommands()