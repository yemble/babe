# http://containertutorials.com/docker-compose/flask-simple-app.html
#MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"

FROM python:2

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential curl vim

COPY  ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./app /opt/app
WORKDIR /opt/app

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["app.py"]

