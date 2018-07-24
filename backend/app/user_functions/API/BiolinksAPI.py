#BiolinksAPI.py
# Margaret Guo 07/23/17
# search gene names on biolinks

import urllib
import requests
import sys
import pprint
import operator

############################################################
# access biolinks api: https://api.monarchinitiative.org/api/
############################################################

class BiolinksAPI:
    API_BASE_URL = 'https://api.monarchinitiative.org/api/search/entity/'
    TIMEOUT_SEC = 30

    @staticmethod
    def query_id(search_term, num_rows=None):
        '''
        Input: 
        search_term <str> entity you want to search the ids for
        num_rows <int> number of rows to search for, if None search all 
        Return: json (dict-like) object with information 

        '''
        if num_rows is None:
            url = BiolinksAPI.API_BASE_URL + search_term 
        else:
            url = BiolinksAPI.API_BASE_URL + search_term + '?rows=' + str(num_rows) + "&start=0"

        # try request
        try:
            res = requests.get(url,
                               timeout=BiolinksAPI.TIMEOUT_SEC)
        except requests.exceptions.Timeout:
            print(url, file=sys.stderr)
            print('Timeout in BiolinksAPI for URL: ' + url, file=sys.stderr)
            return None
 
        # check status code       
        status_code = res.status_code
        if status_code != 200:
            print(url, file=sys.stderr)
            print('Status code ' + str(status_code) + ' for url: ' + url, file=sys.stderr)
            return None
        else:
            return res.json()

    @staticmethod
    def get_best_id(search_term, num_rows=None):
        '''
        Input: 
        search_term <str> entity you want to search the ids for (will return maximum of 20 possibilities)
        num_rows <int> number of rows to search for, if None search all 
        Return: If no terms found, return Nonetype
            Otherwise, return tuple consisting of
                num_found <int> the number of results found
                category_info <dict> key: type (i.e. 'Phenotype', 'disease', etc.) and value: number of eachc category found
                id_info <dict> key: match (str type), value: id (str type), 
        '''
        result = BiolinksAPI.query_id(search_term, num_rows=num_rows)

        if result is not None:
            num_found = result['numFound']
            category_info = dict(result['facet_counts']['category'])
            # print(num_found)
            # print(category_info)

            isGene = max(category_info.items(), key=operator.itemgetter(1))[0] == 'gene'
            id_info = {}
            for idx,( key_id, key_info) in enumerate(result['highlighting'].items()):
                # if gene (the category info with the most returns) must return ncbitype
                # print(key_id, key_info)
                if isGene:
                    if not key_id.startswith('NCBIGene:'):
                        # print(key_id, key_info['match'], '***')
                        # iterate through the result['docs'] looking for the label 
                        for doc in result['docs']:
                            if key_info['match'].lower() == doc['label'][0].lower():
                                if 'equivalent_curie_std' in doc:
                                    for label in doc['equivalent_curie_std']:
                                        if label.startswith('NCBIGene:'):
                                            id_info[key_info['match'].upper()] = label.lower()
                                            # print('found')
                    else:
                        # print(key_id)
                        id_info[key_info['match'].upper()] = key_id.lower()

                else: # if a drug must be a CHEMBL id but can't seem to resolve those with biolinks 

                    id_info[key_info['match']] = key_id
                    # print(result['docs'])


                # print(result['docs'][idx])
            # print(id_info, len(id_info))

            return num_found, category_info, id_info
        else:
            return None       

# if __name__ == "__main__":
#     b = BiolinksAPI()
#     # result = b.query_id('cirrhosis', num_rows=None)
#     result = b.get_best_id('NFKB', num_rows=None)
#     print(result)