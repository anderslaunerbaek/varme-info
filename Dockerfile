FROM python:3.14-slim

# ENV APP_PORT=8080

WORKDIR /app

COPY . ./

RUN pip install -e . --config-settings editable_mode=strict

CMD gunicorn --bind 0.0.0.0:$APP_PORT --workers 4 main:server
