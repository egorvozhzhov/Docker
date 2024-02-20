FROM python:3.10.13-alpine3.18
COPY . /app
WORKDIR /app
RUN pip install flask 
RUN pip install neo4j 
RUN pip install redis  
RUN pip install psycopg2-binary requests

CMD ["python", "app.py"]