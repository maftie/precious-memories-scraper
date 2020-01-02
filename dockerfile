FROM python:2.7.15

WORKDIR /app

COPY requirements.txt ./

COPY ./pmScraper /app/pmScraper

WORKDIR /app

RUN pip install -r /app/requirements.txt
