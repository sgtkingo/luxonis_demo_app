# Dockerfile for Scrapy project
# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /scrapy_project
ENV PYTHONPATH=/scrapy_project
RUN apk add --no-cache linux-headers
COPY . .
EXPOSE 8050

RUN pip install -r requirements.txt
CMD ["scrapy", "crawl", "sreality"]