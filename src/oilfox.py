import requests
from requests.exceptions import HTTPError
import json
import jwt
import time


class api:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        url = "https://api.oilfox.io/v3/login"
        logindata = {"email": self.email, "password": self.password}
        logindata = json.dumps(logindata)
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "User-Agent": "oilfoxpy",
            "Connection": "Keep-Alive",
        }
        response = requests.post(url, data=logindata, headers=headers, timeout=10)
        if response.status_code == 200:
            response = json.loads(response.text)
            self.access_token = response["access_token"]
            self.refreshtoken = response["refresh_token"]
            return True
        elif response.status_code >= 500:
            raise ApiUnreachable
        elif response.status_code == 400:
            raise MalformedCredentials
        elif response.status_code == 401:
            raise RejectedAuthentication
        elif response.status_code == 404:
            raise UserNotFound
        else:
            self.login = False
            return False

    def getsummary(self):
        if hasattr(self, "access_token"):
            self.getrefreshtoken()
            url = "https://api.oilfox.io/v4/summary"
            headers = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Connection": "Keep-Alive",
                "User-Agent": "oilfoxpy",
                "Authorization": "Bearer " + self.access_token,
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                response = json.loads(response.text)
                return response
            # elif(response.status_code == 401):
            #    refreshtoken
            else:
                return False
        else:
            raise InvalidAuthToken
            return False

    def getrefreshtoken(self):
        if hasattr(self, "access_token"):
            dectoken = jwt.decode(self.access_token, verify=False)
            ts = time.time()
            if dectoken["exp"] <= int(ts):
                url = "https://api.oilfox.io/v3/token"
                headers = {
                    "Content-type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "oilfoxpy",
                    "Connection": "Keep-Alive",
                }
                token = {"refresh_token": self.refreshtoken}
                response = requests.post(url, params=token, headers=headers, timeout=10)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    self.access_token = response["access_token"]
                    self.refreshtoken = response["refresh_token"]
                    return True
                else:
                    raise AuthTokenRefreshFailed


class RejectedAuthentication(Exception):
    """Authentication Rejected"""


class UserNotFound(Exception):
    """User not found"""


class MalformedCredentials(Exception):
    """Malformed Credentials (i.e. password too short or invalid mail address)"""


class ApiUnreachable(Exception):
    """API unreachable"""


class AuthTokenRefreshFailed(Exception):
    """AuthToken refresh failed"""


class InvalidAuthToken(Exception):
    """AuthToken invalid or not created"""