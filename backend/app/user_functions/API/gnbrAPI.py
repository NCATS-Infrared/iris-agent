import urllib
import requests
import sys
import pprint

class gnbrAPI:
    API_BASE_URL = 'http://localhost:8080'
    TIMEOUT_SEC = 120

    @staticmethod
    def statements_query(search_term, relations=None, t=None):
    	url = gnbrAPI.API_BASE_URL + '/' + '?' + 's=' + search_term

        if relations:
            url = url + 'r=' + relations

        if t:
            url = url + 't=' + t

        try:
            res = requests.get(url,
                               timeout=gnbrAPI.TIMEOUT_SEC)
        except requests.exceptions.Timeout:
            print(url, file=sys.stderr)
            print('Timeout in QueryGNBR for URL: ' + url, file=sys.stderr)
            return None
        status_code = res.status_code
        if status_code != 200:
            print(url, file=sys.stderr)
            print('Status code ' + str(status_code) + ' for url: ' + url, file=sys.stderr)
            return None
        return res.json()