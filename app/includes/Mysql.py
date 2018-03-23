# Wrapper class for interacting with MariaDB database
# so that we don't have hard-coded queries all over the place
# 
# based on https://gist.github.com/lovesh/7861947

import MySQLdb
import MySQLdb.cursors
# from ... import _config # we could import this directly from the adjacent file, but standards
from . import config as _config

class Cursor(object):
    def __init__(self, mysql_cursor):
        self.cursor = mysql_cursor

    def __iter__(self):
        return self
    
    def next(self):
        row = self.cursor.fetchone()
        if row is None:
            self.cursor.close()
            raise StopIteration
        else:
            return row

class DB(object):
    def __init__(self, host=_config.mysql['host'], username=_config.mysql['user'], password=_config.mysql['passwd'], database=_config.mysql['db']):
        """
        initialises the connection and cursor and returns the connection object
        """
        self.connection = MySQLdb.connect(host=host, user=username, passwd=password, db=database, cursorclass=MySQLdb.cursors.SSDictCursor)
        self._mysql = MySQLdb._mysql

    def _execute(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        except self._mysql.OperationalError:
            self.__init__()
            cursor = self.connection.cursor()
            cursor.execute(query)
        return cursor

    def _executemany(self, query, values):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query)
        except self._mysql.OperationalError:
            self.__init__()
            cursor = self.connection.cursor()
            cursor.executemany(query, values)
        return cursor

    def getRows(self, query):
        """
        returns the iterator on the resultset of the query (lazy reading)
        """
        cursor = self._execute(query)
        return Cursor(cursor)

    def getManyRows(self, query, limit=None):
        """
        returns the tuple of rows of the query result where each row is a dictionary with column names as keys
        """
        cursor = self._execute(query)
        if limit:
            rows = cursor.fetchmany(limit)
        else:
            rows = cursor.fetchall()
        cursor.close()
        return rows

    def getSingleRow(self, query):
        """
        returns the row as a dictionary with column names as keys
        """
        cursor = self._execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    def insertManyRows(self, table, data, commit=True):
        """
        insert multiple rows into table
        data is a dictionary with keys as column names and the values are the values to insert
        e.g. data = {
            'firstname': ['Aleks', 'Anna', 'Sarah'],
            'lastname': ['Christensen', 'Zaitzeff', 'Olson']
        }
        would turn into `INSERT INTO table (firstname, lastname) VALUES (('Aleks', 'Christensen'), ('Anna', 'Zaitzeff'), ('Sarah', 'Olson'))`
        """
        if len(set(len(value_tuple) for value_tuple in data.values())) > 1:
            raise Exception('All value tuples of data should be of the same length')
        columns, values = [], map(lambda x: [], data)
        for key, val in data.items():
            columns.append(key)
            for index, item in enumerate(val):
                values[index].append(item)
        values = map(tuple, values)
        format_specifier_string = ('%s, '*len(columns)).strip(', ')
        query = "INSERT INTO %s (%s) VALUES (%s)" % (table, ', '.join(columns), format_specifier_string)
        cursor = self._executemany(query, values)
        self.last_insert_id = self.connection.insert_id()
        if commit:
            self.connection.commit()
        cursor.close()

    def execute(self, query, commit=True, raise_exceptions=False):
        """
        execute the CRUD query
        """
        tries = 0
        while tries < 2:
            try:
                cursor = self._execute(query)
                self.last_insert_id = self.connection.insert_id()
                if commit:
                    self.connection.commit()
                cursor.close()
                return
            except Exception as e:
                print e
                tries += 1
                if raise_exceptions:
                    raise e
                pass
        print 'query aborted because of exception'
        cursor.close()

    def commit(self):
        """
        commit the uncommitted queries
        """
        self.last_insert_id = self.connection.insert_id()
        self.connection.commmit()

    def close(self):
        """
        close connection
        """
        self.connection.close()

    def escape_string(self, string):
        return MySQLdb.escape_string(string)

class Mysql(DB):
    def __init__(self):
        super(Mysql, self).__init__()
