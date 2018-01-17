import requests
requests.adapters.DEFAULT_RETRIES = 2
class API:
    
    access_token = False
    sid = False
    #URL = "https://my.rainmachine.com/s/{}/{}?access_token={}"
    URI = "10.10.106.71:8080"
    URL = "https://{}/api/4/{}?access_token={}"

    email = "salsahonor@gmail.com"
    pwd = "strong password"

    init = False

    # Have to use a session because Rainmachine uses a cookie to authenticate
    session = requests.Session()

    def __init__(self):
        self.init = self.auth()
        
    # Function to get access token and cookie immediatley
    def auth(self):
        #data = '''{
        #    "user": {
        #        "email": "anna.zaitzeff@gmail.com",
        #        "pwd": "strong password",
        #        "remember": false
        #    }
        #}'''
        data = '''{
            "pwd": "strong password",
            "remember": 0
        }'''

        #req = self.session.post("https://my.rainmachine.com/login/auth", data=data, headers={"Content-Type": "application/json"})
        try:
	    req = self.session.post("https://{}/api/4/auth/login".format(self.URI), data=data, headers={"Content-Type": "application/json"}, verify=False)
            res = req.json()
            if res["statusCode"] == 0:
                self.access_token = res['access_token']
                #self.sid = res['sprinklerId']
                return {"error": 0, "message": "success"}
            else:
                return {"error": 1, "message": "Error authenticating with Rainmachine API"}
        except requests.exceptions.RequestException:
            return {"error": 2, "message": "Error reading received JSON object"}

    # Since we need the cookie to work, just handle all Rainmachine API calls
    # through this class instead of the controller
    def get(self, endpoint):
        #url = self.URL.format(self.sid, endpoint, self.access_token)
        url = self.URL.format(self.URI, endpoint, self.access_token)

        req = self.session.get(url)

        try:
            return {"error": 0, "result": req.json()}
        except ValueError:
            return {"error": 3, "message": "Error reading received JSON object"}

    def post(self, endpoint, data=None):
        #url = self.URL.format(self.sid, endpoint, self.access_token)
        url = self.URL.format(self.URI, endpoint, self.access_token)

        req = self.session.get(url, data=data)

        try:
            return {"error": 0, "result": req.json()}
        except ValueError:
            return {"error": 4, "message": "Error reading received JSON object"}
