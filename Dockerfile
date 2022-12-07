FROM python:3.8.15-alpine3.16

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc g++ libxml2-dev libxslt-dev python3-dev \
    && pip install --upgrade pip


COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./
    
CMD python metrobus/manage.py makemigrations estaciones;python metrobus/manage.py migrate estaciones;python metrobus/data.py metrobus/mb_kmz;python metrobus/manage.py runserver 0.0.0.0:8000

