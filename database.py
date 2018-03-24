import MySQLdb

# Make sure to sudo pip install -r requirements.txt again if you haven't recently. 
#You'll need mysql on your computer as well as mysql-python (mixed OS) or python-mysqldb (ubuntu)
# Open database connection ( If database is not created just leave "yourdbname"as it is.)
db = MySQLdb.connect(user="root",db="mysql")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# For creating create db
# Below line  is hide your warning
cursor.execute("SET sql_notes = 0; ")
# create db here....
cursor.execute("create database IF NOT EXISTS SmartCity")
cursor.execute("USE SmartCity")

# create table
cursor.execute("SET sql_notes = 0; ")
cursor.execute("CREATE TABLE IF NOT EXISTS users (userid int(11) NOT NULL AUTO_INCREMENT, firstname varchar(20), lastname varchar(20), dept varchar(15), username varchar(15), password varchar(32), roles varchar(10000), PRIMARY KEY (userid));")
cursor.execute("SET sql_notes = 1; ")

# insert data into the table. The hash is the word "password" using MD5.
cursor.execute("insert into users (username, password) values('admin','5f4dcc3b5aa765d61d8327deb882cf99');")

# create a new user that only has privileges for that specific database.
cursor.execute("create user 'smartcity'@'localhost';")
cursor.execute("grant all privileges on SmartCity.* to 'smartcity'@'localhost' identified by 'manydevices';")

# Commit your changes in the database
db.commit()

# disconnect from server
db.close()
