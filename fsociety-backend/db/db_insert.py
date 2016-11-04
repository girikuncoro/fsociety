import os
import pickle
import re
import sys
import MySQLdb as mysql

DB_HOST = '10.2.13.60'
#DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'fsociety'
DB_PASS = 'vmware@123'
#DB_PASS = ''
DB_NAME = 'hackme'

#REUTER_FILE = 'reuters_sentences.list'

def insert_in_db(filename):
	# Open database connection
	db = mysql.connect(host=DB_HOST, port=DB_PORT,
	        user=DB_USER, passwd=DB_PASS,
	        db=DB_NAME)

	# Create new db cursor
	cursor = db.cursor()

	# Load the sentences from the pickle file
	sentences = pickle.load(open(filename,'rb'))

	sql = 'DROP TABLE IF EXISTS `sentence`'
	try:
	    cursor.execute(sql)
	    db.commit()
	except mysql.Error as err:
	    print("Something went wrong: {}".format(err))
	    db.rollback()

	sql = 'CREATE TABLE `sentence`(sen_id int not null auto_increment, content varchar(10000) not null, primary key (sen_id))'
	try:
	    cursor.execute(sql)
	    db.commit()
	except mysql.Error as err:
	    print("Something went wrong: {}".format(err))
	    db.rollback()
	
	for sentence in sentences:
		sen = ''
		for word in sentence:
			sen += word + ' '
		sen = re.sub("\"", "\'", sen)

		sql = 'INSERT INTO `sentence`(`content`) VALUES (\"' + sen + '\")'

		# insert to the database
		try:
		    cursor.execute(sql)
		    db.commit()
		except mysql.Error as err:
		    print("Something went wrong: {}".format(err))
		    db.rollback()


	# Close the DB connection
	db.close()

if len(sys.argv) > 1:
	filename = sys.argv[1]
	print filename
	insert_in_db(filename)
else:
	print "Enter filename as an argument"
	sys.exit(1)