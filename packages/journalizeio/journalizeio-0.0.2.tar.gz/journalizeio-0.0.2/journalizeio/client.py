import requests


class JournalizeClient(object):
    BASE_URL = "https://api.journalize.io"

    def __init__(self, api_key):
        self.api_key = api_key

    def ping(self):
        rc = requests.get(self.BASE_URL + "/ping")
        return rc.json()
