FROM python:3.10-alpine

ENV HOSTNAME_TARGET=localhost
ENV PORT_TARGET=8080

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install -r ./requirements.txt

COPY ./app /app
COPY ./.env /.env

CMD [ "python", "/app/app.py" ]