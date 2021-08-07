# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /marshall
COPY .. .
RUN python -m venv denv
RUN . denv/bin/activate \
 && pip install --upgrade pip
RUN . denv/bin/activate \
 && pip install -r requirements.txt
RUN python marshall.py