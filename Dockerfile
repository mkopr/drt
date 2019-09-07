FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /service
WORKDIR /service
ADD requirements.txt /service/
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
ADD . /service/