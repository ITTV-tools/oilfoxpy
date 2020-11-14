import requests
from requests.exceptions import HTTPError
import json
import jwt
import time

class api():
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        url = "https://api.oilfox.io/v3/login"
        logindata = {
            "email": self.email,
            "password": self.password
        }
        logindata = json.dumps(logindata)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json','User-Agent': 'oilfoxpy', 'Connection': 'Keep-Alive'}
        response = requests.post(url, data=logindata, headers=headers, timeout=10)
        if(response.status_code == 200):
            response = json.loads(response.text)
            self.access_token = response['access_token']
            self.refreshtoken = response['refresh_token']
            return True
        elif(response.status_code == 401):
            raise oilfoxerror('Check Login Data')
        else:
            self.login = False
            return False


    def getSummery(self):
        if(hasattr(self, 'access_token')):
            self.reqrefreshtoken()
            url= "https://api.oilfox.io/v4/summary"
            headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Connection': 'Keep-Alive','User-Agent': 'oilfoxpy', 'Authorization': 'Bearer ' + self.access_token}
            response = requests.get(url, headers=headers, timeout=10)
            if(response.status_code == 200):
                response = json.loads(response.text)
                return response
            #elif(response.status_code == 401):
            #    refreshtoken
            else:
                return False
        else:
            raise oilfoxerror('Login first')
            return False

    def reqrefreshtoken(self):
        if(hasattr(self, 'access_token')):
            dectoken = jwt.decode(self.access_token, verify=False)
            ts = time.time()
            if(dectoken['exp'] <= int(ts)):
                url = "https://api.oilfox.io/v3/token"
                headers = {'Content-type': 'application/json', 'Accept': 'application/json','User-Agent': 'oilfoxpy', 'Connection': 'Keep-Alive'}
                token = {
                    'refresh_token': self.refreshtoken
                }
                response = requests.post(url, params=token, headers=headers, timeout=10)
                if(response.status_code == 200):
                    response = json.loads(response.text)
                    self.access_token = response['access_token']
                    self.refreshtoken = response['refresh_token']
                    return True
                else:
                    raise oilfoxerror('failed tokenrefresh')

class oilfoxerror(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'Oilfox, {0} '.format(self.message)
        else:
            return 'Oilfox error'
