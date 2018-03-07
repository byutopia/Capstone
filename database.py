import MySQLdb

# Make sure to sudo pip install -r requirements.txt again if you haven't recently. 
#You'll need mysql on your computer as well as mysql-python (mixed OS) or python-mysqldb (ubuntu)
# Open database connection ( If database is not created just leave "yourdbname"as it is.)
db = MySQLdb.connect("localhost", "root", "password", "capstone" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# For creating create db
# Below line  is hide your warning
cursor.execute("SET sql_notes = 0; ")
# create db here....
cursor.execute("create database IF NOT EXISTS capstone")

# create table
cursor.execute("SET sql_notes = 0; ")
cursor.execute("create table IF NOT EXISTS users (username varchar(200),password char(32));")
cursor.execute("SET sql_notes = 1; ")

# insert data into the table. The hash is the word "password" using MD5.
cursor.execute("insert into users (username,password) values('user','5f4dcc3b5aa765d61d8327deb882cf99');")

# create a new user that only has privileges for that specific database.
cursor.execute("create user 'admin'@'localhost';")
cursor.execute("grant all privileges on capstone.* to 'admin'@'localhost' identified by 'strong password';")

# Commit your changes in the database
db.commit()

# disconnect from server
db.close()
