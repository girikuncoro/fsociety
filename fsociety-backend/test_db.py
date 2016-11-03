import MySQLdb as mysql
from faker import Factory
import os

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', '10.2.13.60')
ROJAK_DB_PORT = int(os.getenv('ROJAK_DB_PORT', 3306))
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'fsociety')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'vmware@123')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'sample')

# Open database connection
db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
        user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS,
        db=ROJAK_DB_NAME)

# Create new db cursor
cursor = db.cursor()

insert_sql = '''
INSERT INTO `test`(`id`, `name`)
VALUES (12, 'asd');
'''

# insert to the database
try:
    cursor.execute(insert_sql)
    db.commit()
except mysql.Error as err:
    print("Something went wrong: {}".format(err))
    db.rollback()


# Close the DB connection
db.close()

