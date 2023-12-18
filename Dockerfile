FROM --platform=arm64 python:3.10-alpine

ENV HOSTNAME=0.0.0.0
ENV PORT=12345
ENV HOSTNAME_TARGET=localhost
ENV PORT_TARGET=8080

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install -r ./requirements.txt

COPY ./app /app

CMD [ "python", "/app/app.py" ]