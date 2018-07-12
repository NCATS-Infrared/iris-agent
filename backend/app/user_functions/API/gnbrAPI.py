import urllib
import requests
import sys
import pprint

class gnbrAPI:
    API_BASE_URL = 'http://localhost:8080'
    TIMEOUT_SEC = 120