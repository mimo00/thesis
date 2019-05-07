FROM python:3.7

RUN make /tmp

ADD thesis /opt/thesis
WORKDIR /opt/thesis

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# script that allows us to wait for database before starting django server
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /usr/bin/
RUN chmod +x /usr/bin/wait-for-it.sh

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;
