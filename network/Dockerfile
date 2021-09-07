FROM postgres:latest
COPY . .
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.9-dev
RUN apt-get install postgresql-server-dev-10 gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt
RUN cd engine
RUN python __init__.py
USER postgres
EXPOSE 8008
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]