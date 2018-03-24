# class to handle database calls instead of direct queries

from hashlib import md5
import Mysql

class DBC():
    def __init__(self):
        self.database = Mysql.Mysql()

    """
    Check if credentials are valid
    Status codes:
     0: success
     1: missing username or password
     2: invalid credentials
     -1: something else
    """
    def loginCheck(self, username, password):
        if not username or not password:
            return {'status': 1}
        try:
            check = self.database.getSingleRow("SELECT COUNT(1) FROM users WHERE username = '{usr}' AND password = MD5('{pwd}')".format(usr=username, pwd=password))
            if check:
                data = self.database.getSingleRow("SELECT firstname, roles FROM users WHERE username = '{}'".format(username))
                return {'status': 0, 'data': data}
            else:
                return {'status': 2}
        except:
            import sys
            return {'status': -1, 'message': sys.exc_info()[1]}

