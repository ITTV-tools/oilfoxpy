import requests
import json

class api:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.access_token = ""

    def login(self):
        url = "https://api.oilfox.io/v3/login"
        logindata = {
            "email": self.email,
            "password": self.password
        }
        logindata = json.dumps(logindata)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Connection': 'Keep-Alive'}
        response = requests.post(url, data=logindata, headers=headers, timeout=10)        
        response = json.loads(response.text)
        self.access_token = response['access_token']
        return True


    def getSummery(self):
        url= "https://api.oilfox.io/v4/summary"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Connection': 'Keep-Alive', 'Authorization': 'Bearer ' + self.access_token}
        response = requests.get(url, headers=headers, timeout=10)
        response = json.loads(response.text)
        return response