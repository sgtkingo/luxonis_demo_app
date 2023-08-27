# Dockerfile for Flask app
# syntax=docker/dockerfile:1
FROM python:3.11-alpine
WORKDIR /flask_app
ENV PYTHONPATH=/flask_app
RUN apk add --no-cache linux-headers
COPY . .
EXPOSE 5000

RUN pip install -r requirements.txt
CMD ["flask", "run"]