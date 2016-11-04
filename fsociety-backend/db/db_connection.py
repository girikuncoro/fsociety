import MySQLdb as mysql
import os
import pickle
import re

DB_HOST = '10.2.13.60'
#DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'fsociety'
DB_PASS = 'vmware@123'
#DB_PASS = ''
DB_NAME = 'hackme'

REUTER_FILE = 'reuters_sentences.list'

def insert_in_db(filename):
	# Open database connection
	db = mysql.connect(host=DB_HOST, port=DB_PORT,
	        user=DB_USER, passwd=DB_PASS,
	        db=DB_NAME)

	# Create new db cursor
	cursor = db.cursor()

	# Load the sentences from the pickle file
	sentences = pickle.load(open(filename,'rb'))

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

def get_sentences(ids):
	# Open database connection
	db = mysql.connect(host=DB_HOST, port=DB_PORT,
	        user=DB_USER, passwd=DB_PASS,
	        db=DB_NAME)

	# Create new db cursor
	cursor = db.cursor()
	sentences = []

	for id in ids:
		sql = 'SELECT `content` FROM `sentence` WHERE SEN_ID = %d' % id
		cursor.execute(sql)
		sentences.append(cursor.fetchall())

	return sentences
	#try:
	#    db.commit()
	#except mysql.Error as err:
	 #   print("Something went wrong: {}".format(err))
	  #  db.rollback()

#insert_in_db(REUTER_FILE)
#ids = [1,2,3]
#sentences = get_sentences(ids)
#print len(sentences)
#print sentences