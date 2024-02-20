FROM python:3.10.13-alpine3.18

COPY . /app
WORKDIR /app
RUN pip install flask neo4j psycopg2-binary redis elasticsearch requests

CMD ["python", "app.py"]