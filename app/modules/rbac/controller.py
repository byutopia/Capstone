import mysql.connector
from mysql.connector import Error
# from python_mysql_dbconfig import read_db_config
# rbac_mod = Blueprint('rbac', __name__)
# @rbac_mod.route('rbac',methods = ['GET'])

def query_with_fetchone():
        try:
            conn = mysql.connector.connect(host='localhost', database='SmartCity', user='user1', password='password')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                row = cursor.fetchone()
                while row is not None:
                    print(row)
                    row = cursor.fetchone()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
if __name__ == '__main__':
    query_with_fetchone()
