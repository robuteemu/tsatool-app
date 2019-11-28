FROM python:3.7-slim-buster as base                                                                                              

COPY . /app                                                                                                         
WORKDIR /app
RUN apt-get update && \
  apt-get install -y gcc gfortran wget libpq-dev \
  libfreetype6-dev libpng-dev glibc-source libxml2-dev libxslt-dev \
  libjpeg-dev zlib1g-dev libtiff-dev tk-dev tcl-dev && \
  ln -s /usr/include/locale.h /usr/include/xlocale.h && \
  pip install -r requirements.txt

ENV PG_HOST=timescaledb
ENV PG_PASSWORD=jyxT9AaWA884t6c6s9AZ
ENV PG_USER=tsadash
