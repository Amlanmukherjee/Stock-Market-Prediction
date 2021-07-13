FROM ubuntu:18.04
WORKDIR /app 
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip setuptools wheel
COPY . /app
COPY . /flask
RUN pip3 install -r requirements.txt
CMD ["uwsgi", "app.ini"]