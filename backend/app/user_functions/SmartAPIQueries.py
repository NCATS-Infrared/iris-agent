
'''
Commands to perform basic queries in SmartAPI
'''


from iris import state_types as t
from iris import IrisCommand

from iris import state_machine as sm
from iris import util as util
from iris import iris_objects
from user_functions.API import SmartAPI

# class ListAllKnowledgeSources(IrisCommand):
#     title = "What knowledge sources are available in SmartAPI?"
#     examples = ["What knowledge sources available?",
#                 "What databases are available?",
#                 "What resources are available?"]


#     def command(self):
#         s = SmartAPI.SmartAPI()
#         result = s.search_all('*')
#         return result

#     def explanation(self, result):
#         return result


# ListAllKnowledgeSources = ListAllKnowledgeSources()

class ListAllTags(IrisCommand):
    title = "What kinds of information do you have?"
    examples = ["What kinds of information are available?",
                "What type of information is available?",
                "What tags exist?"]


    def command(self):
        s = SmartAPI.SmartAPI()
        result = s.search_all_tags()
        return result

    def explanation(self, result):
        return result


ListAllTags = ListAllTags()

# class SearchKnowledgeSourceTitles(IrisCommand):
#     title = "What knowledge source titles include {query}?"
#     examples = ["What knowledge sources titles contain {query}?"]

#     argument_types = {"query": t.String("What is the search term?")}

#     def command(self, query):
#         s = SmartAPI.SmartAPI()
#         result = s.search_titles(query)
#         return result # returns list 

#     def explanation(self, result):
#         if len(result)> 0:
#             return result
#         else:
#             return 'No source titles found'

# SearchKnowledgeSourceTitles = SearchKnowledgeSourceTitles()


class SearchKnowledgeSourceFull(IrisCommand):
    title = "What knowledge sources include information about {query}?"
    examples = ["What knowledge sources discuss {query}?",
                "What sources in SmartAPI talk about {query}?"]

    argument_types = {"query": t.String("What is the search term?")}

    def command(self, query):
        s = SmartAPI.SmartAPI()
        df_name = query
        result = s.search_tags(query)
        result_array = [] # code added for df test
        for r in result:
            result_array.append(r['title']) # code added for df test
        # result_df = iris_objects.IrisDataframe(data=result_array) # code added for df test
        self.iris.add_to_env(df_name, result_array) # code added for df test
        return result

    def explanation(self, result):
        if len(result)> 0:
            processed_result = []
            for r in result:
                text = r['title'] 
                if r['description'] != 'Missing':
                    text += "\n\nDescription: " + r['description']
                text += "\n\nTags: "
                tags = r['tags']
                for i in range(len(tags)):
                    if i < len(tags) - 1:
                        text += tags[i] + ", "
                    else:
                        text += tags[i]
                processed_result.append(text)
            return processed_result
        else:
            return 'No knowledge sources found'

SearchKnowledgeSourceFull = SearchKnowledgeSourceFull()

class QueryInformationAboutNode(IrisCommand):
    title = "Query information about {entity}"
    examples = ["Give me information about {entity}",
                "Tell me about {entity}"]
    argument_types = {
        "entity": t.EnvVar("What type of entity do you want to know about?"),
        "index": t.Int("Which knowledge source do you want to use?")
    }

    def command(self, entity : t.EnvVar, index):
        if index > 0 and index <= len(entity):
            self.iris.add_to_env("selected_api", entity[index-1])
            return entity[index-1]
        return

    def explanation(self, result):
        return "Selected: " + result

QueryInformationAboutNode = QueryInformationAboutNode()

class QueryInformationAboutNodeHelper(IrisCommand):
    title = "What information do you have about {entity_name}?"
    examples = ["What do you know about {entity_name}?",
                "What can you tell me about {entity_name}?"]

    argument_types = {"entity_name": t.String("What is the search term?")}

    def command(self, entity_name):
        s = SmartAPI.SmartAPI()
        api = self.iris.env["selected_api"].replace(" ", "&")
        result = s.query_api(api, entity_name)
        return result

    def explanation(self, result):
        return result

QueryInformationAboutNodeHelper = QueryInformationAboutNodeHelper()