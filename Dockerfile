# http://containertutorials.com/docker-compose/flask-simple-app.html
#MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"

FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential curl vim

COPY  . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]

