FROM python:3.10.13-alpine3.18

COPY . /app
WORKDIR /app
RUN pip install flask py2neo requests

CMD ["python", "app.py"]