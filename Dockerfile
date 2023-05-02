FROM python:3-slim

WORKDIR /app

COPY . /app

CMD [ "python", "PA2.py", "<", "PA2_test.sql"]

