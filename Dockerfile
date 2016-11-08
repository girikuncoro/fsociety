FROM ubuntu:latest
MAINTAINER fsociety
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libmysqlclient-dev nginx

# RUN echo "mysql-server mysql-server/root_password password root" | sudo debconf-set-selections
# RUN echo "mysql-server mysql-server/root_password_again password root" | sudo debconf-set-selections

#RUN apt-get install -y mysql-server

#RUN ufw allow 'Nginx HTTP'
RUN mkdir /usr/share/nginx/logs && touch /usr/share/nginx/logs/static.log
COPY . /app
ADD  ./fsociety-frontend/nginx.conf /etc/nginx/conf.d/default.conf

#update pip
RUN pip install --upgrade pip
#satisfy requirements
RUN pip install -r /app/fsociety-backend/requirements.txt

EXPOSE 80

#CMD ["/bin/bash"]

CMD sh /app/init.sh
