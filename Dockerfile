FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask mysql-connector-python

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
