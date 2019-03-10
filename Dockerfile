FROM python:3.7

ADD thesis /opt/thesis
WORKDIR /opt/thesis

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# script that allows us to wait for database before starting django server
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /usr/bin/
RUN chmod +x /usr/bin/wait-for-it.sh

