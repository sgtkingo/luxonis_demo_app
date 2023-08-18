# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /app
ENV PYTHONPATH=/app
RUN apk add --no-cache linux-headers
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 5432
CMD ["sh", "-c", "cd ./engine/ && scrapy crawl test && cd .. && flask run"]