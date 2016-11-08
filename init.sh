/etc/init.d/nginx start
#/etc/init.d/mysql start


#mysql -h localhost -u root --password='root' -e "CREATE DATABASE IF NOT EXISTS hackme;"

#db
#python /app/fsociety-backend/db/db_insert.py reuters_sentences.list

#fire the back-end
python /app/fsociety-backend/app.py

sh /bin/bash

#fire the http server
#cd /app/fsociety-frontend

#fire front-end
#python -m SimpleHTTPServer 8000
