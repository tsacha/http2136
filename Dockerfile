FROM python:latest
    MAINTAINER Sacha Trémoureux <sacha@tremoureux.fr>

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN \
   apt -y update && \
   apt -y --no-install-recommends install dnsutils && \
   pip install --no-cache-dir -r requirements.txt
COPY main.py .

CMD uvicorn --host '' --port 8000 --proxy-headers main:app
