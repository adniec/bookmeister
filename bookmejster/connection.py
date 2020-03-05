import requests
from json import dumps, loads


class Database:

    def __init__(self):
        self.url = "https://bookstore-5217.restdb.io/rest/books"
        self.headers = {
            'content-type': "application/json",
            'x-apikey': "5e5f9cf028222370f14d4ece",
            'cache-control': "no-cache"
        }

    def add(self, values):
        try:
            requests.request("POST", self.url, data=dumps(values), headers=self.headers)
        except:
            return False
        return True

    def search(self, parameters):
        query = f'?q={dumps(parameters)}'
        try:
            response = requests.request("GET", self.url + query, headers=self.headers)
            return loads(response.text)
        except:
            return None

    def delete(self, id):
        try:
            response = requests.request("DELETE", self.url + '/' + id, headers=self.headers)
        except:
            return False
        return True if id in response.text else False

    def update(self, id, values):
        try:
            response = requests.request("PATCH", self.url + '/' + id, data=dumps(values), headers=self.headers)
        except:
            return False
        return True if id in response.text else False
