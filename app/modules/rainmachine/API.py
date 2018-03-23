import requests
import urllib3
from ... import _config
requests.adapters.DEFAULT_RETRIES = 2
requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class API():

    def __init__(self):
        self.access_token = False
        self.sid = False
        self.URI = _config.rainmachine['address'] + ":8080"
        self.URL = "https://{}/api/4/{}?access_token={}"

        self.email = _config.rainmachine['email']
        self.pwd = _config.rainmachine['pwd']

        # Have to use a session because Rainmachine uses a cookie to authenticate
        self.session = requests.Session()

        self.init = self.auth()

    # Function to get access token and cookie immediatley
    def auth(self):
        # since this string will be formatted, the data needs double brackets
        # because otherwise python will try to format the whole thing
        data = '''{{
            "pwd": "{0}",
            "remember": 0
        }}'''

        try:
	    req = self.session.post("https://{}/api/4/auth/login".format(self.URI), data=data.format(self.pwd), headers={"Content-Type": "application/json"}, verify=False, timeout=3)
            res = req.json()
            if res["statusCode"] == 0:
                self.access_token = res['access_token']
                return {"error": 0, "message": "success"}
            else:
                return {"error": 1, "message": "Error authenticating with Rainmachine API"}
        except ValueError:
            return {"error": 2, "message": "Error reading received JSON object"}
        except requests.exceptions.RequestException:
            return {"error": 3, "message": "Error connecting to Rainmachine"}

    # Since we need the cookie to work, just handle all Rainmachine API calls
    # through this class instead of the controller
    def get(self, endpoint):
        url = self.URL.format(self.URI, endpoint, self.access_token)
        req = self.session.get(url, timeout=3, verify=False)

        try:
            return {"error": 0, "result": req.json()}
        except ValueError:
            return {"error": 3, "message": "Error reading received JSON object"}

    def post(self, endpoint, data=None):
        url = self.URL.format(self.URI, endpoint, self.access_token)
        req = self.session.post(url, data=data, headers={"Content-Type": "application/json"}, timeout=3, verify=False)

        try:
            return {"error": 0, "result": req.json()}
        except ValueError:
            return {"error": 4, "message": "Error reading received JSON object"}
