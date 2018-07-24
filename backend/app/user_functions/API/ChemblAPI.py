# # ChemblAPI.py
# # Margaret Guo 07/23/17
# # make a ChemblAPI to search for drug names
# # need https://github.com/chembl/chembl_webresource_client

# import urllib
# import requests
# import sys
# import pprint
# import operator
# import sys, json
# from xml.etree import ElementTree

# from chembl_webresource_client.new_client import new_client
# molecule = new_client.molecule
# res = molecule.search('zestril')
# print(res)
# # # from chembl_webresource_client.new_client import new_client
# # ############################################################
# # # access MESH:  https://www.ebi.ac.uk/chembl/api/data/docs
# # ############################################################

# # class ChemblAPI:
# #     API_BASE_URL = 'https://www.ebi.ac.uk/chembl/api/data/molecule/search?q='
# #     TIMEOUT_SEC = 30


# #     @staticmethod
# #     def query_id(search_term):
# #         '''
# #         Input: 
# #         search_term <str> entity you want to search the ids for
# # 		OUtput:

# #         '''
# #         # preprocess search term
# #         search_term = search_term.lower()
# #         search_term = ("%20").join(search_term.split(' '))
# #         print(search_term)
# #         url = ChemblAPI.API_BASE_URL + search_term 
# #         # try request
# #         try:
# #             res = requests.get(url,
# #                                timeout=ChemblAPI.TIMEOUT_SEC)
# #         except requests.exceptions.Timeout:
# #             print(url, file=sys.stderr)
# #             print('Timeout in ChemblAPI for URL: ' + url, file=sys.stderr)
# #             return None
 
# #         # check status code       
# #         status_code = res.status_code
# #         if status_code != 200:
# #             print(url, file=sys.stderr)
# #             print('Status code ' + str(status_code) + ' for url: ' + url, file=sys.stderr)
# #             return None
# #         else:

# #             print(res, type(res))


# #             result = res.text
# #             print(result)
# #             tree = ElementTree.fromstring(result)
# #             print(tree)
# #             return result
# #             # # contains lists of dict with the following keys: d, dname, c, cname; GNBR uses d and dname
# #             # output_dict = {}
# #             # for mesh in result:
# #             # 	mesh_id_raw = mesh['d']['value'].split('/')[-1]
# #             # 	mesh_id = 'MESH:' + mesh_id_raw
# #             # 	mesh_name = mesh['dName']['value']
# #             # 	output_dict[mesh_name] = mesh_id

# #             # return output_dict

# # if __name__ == "__main__":
# #     b = ChemblAPI()
# #     result = b.query_id('warfarin')
# #     # print(result)