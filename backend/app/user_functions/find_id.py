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
	        id_object = iris_objects.IrisDataframe(data=[list(item) for item in id_info.items()], column_names = ["Name", "ID"] )
	        id_name = 'id_' + entity
	        self.iris.add_to_env(id_name, id_object)    
        	return [text, id_object]            
        else:
        	return text

_FindID = FindID()