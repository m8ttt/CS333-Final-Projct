FROM python:3-slim

WORKDIR /app

COPY . /app

COPY PA2_test.sql /app/PA2_test.sql

CMD bash -c "cat PA2_test.sql | python PA2.py"


