# MeshAPI.py
# Margaret Guo 07/23/17

# uses the SPARQL Query to get a json with possible MESH ids

import urllib
import requests
import sys
import pprint
import operator

############################################################
# access MESH:  https://id.nlm.nih.gov/mesh/query?query=
############################################################

class MeshAPI:
    PRE_BASE_URL = 'https://id.nlm.nih.gov/mesh/sparql?query=PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX%20xsd%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX%20owl%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX%20meshv%3A%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2Fvocab%23%3E%0D%0APREFIX%20mesh%3A%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F%3E%0D%0APREFIX%20mesh2015%3A%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2015%2F%3E%0D%0APREFIX%20mesh2016%3A%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2016%2F%3E%0D%0APREFIX%20mesh2017%3A%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2017%2F%3E%0D%0APREFIX%20mesh2018%3A%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2018%2F%3E%0D%0A%0D%0ASELECT%20%3Fd%20%3FdName%20%3Fc%20%3FcName%20%0D%0AFROM%20%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%3E%0D%0AWHERE%20%7B%0D%0A%20%20%3Fd%20a%20meshv%3ADescriptor%20.%0D%0A%20%20%3Fd%20meshv%3Aconcept%20%3Fc%20.%0D%0A%20%20%3Fd%20rdfs%3Alabel%20%3FdName%20.%0D%0A%20%20FILTER(REGEX(%3FdName%2C%27'
    POST_BASE_URL = '%27%2C%27i%27))%20%0D%0A%7D%20%0D%0AORDER%20BY%20%3Fd%20%0D%0A&format=JSON&limit=50&offset=0&inference=true'
    TIMEOUT_SEC = 60

    @staticmethod
    def query_id(search_term):
        '''
        Input: 
        search_term <str> entity you want to search the ids for
        Output: if found
        output_dict: <dict>: 
            key <str> name associated with id, value <str> MESH ID
        '''
        # preprocess search term
        search_term = search_term.lower()
        search_term = ("%20").join(search_term.split(' '))
        print(search_term)
        url = MeshAPI.PRE_BASE_URL + search_term + MeshAPI.POST_BASE_URL
        # try request
        try:
            res = requests.get(url,
                               timeout=MeshAPI.TIMEOUT_SEC)
        except requests.exceptions.Timeout:
            print(url, file=sys.stderr)
            print('Timeout in MeshAPI for URL: ' + url, file=sys.stderr)
            return None
 
        # check status code       
        status_code = res.status_code
        if status_code != 200:
            print(url, file=sys.stderr)
            print('Status code ' + str(status_code) + ' for url: ' + url, file=sys.stderr)
            return None
        else:
            result = res.json()['results']['bindings']

            # contains lists of dict with the following keys: d, dname, c, cname; GNBR uses d and dname
            output_dict = {}
            for mesh in result:
            	mesh_id_raw = mesh['d']['value'].split('/')[-1]
            	mesh_id = 'MESH:' + mesh_id_raw
            	mesh_name = mesh['dName']['value']
            	output_dict[mesh_name] = mesh_id

            return output_dict

if __name__ == "__main__":
    import pandas as pd
    b = MeshAPI()
    result = b.query_id('furosemide')
    print(result)
    df_id = pd.DataFrame.from_dict(result, orient='index', dtype=None, columns=["ID"])
    print(df_id)
#     