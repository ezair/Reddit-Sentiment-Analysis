FROM ubuntu:18.04

# Installing mongodb.
RUN apt-get update && apt-get install -y gnupg2
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
RUN echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu/ xenial/mongodb-org/3.4 multiverse" |  tee /etc/apt/sources.list.d/mongodb-3.4.list
RUN apt-get update && apt-get install -y mongodb-org
RUN mkdir -p /data/db
RUN chown -R mongodb:mongodb /data/db
VOLUME ["/data/db"]
EXPOSE 27017

#Install doxygen for documentation.
RUN apt-get install -y doxygen

# Installing python3 and setting up all needed packages for it.
FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt .
RUN pip install -U setuptools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code
