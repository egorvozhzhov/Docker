FROM python:3.10.13-alpine3.18

COPY . /app
WORKDIR /app
RUN pip install flask neo4j py2neo redis requests

CMD ["python", "app.py"]