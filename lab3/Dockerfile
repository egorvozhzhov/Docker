FROM python:3.10.13-alpine3.18
COPY . /app
WORKDIR /app
RUN pip install flask 
RUN pip install redis  
RUN pip install psycopg2-binary requests py2neo

CMD ["python", "app.py"]