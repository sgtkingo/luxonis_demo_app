# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /app
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
WORKDIR /app/engine
RUN scrapy crawl test
WORKDIR /app
CMD ["flask", "run"]