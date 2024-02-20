import psycopg2
from elasticsearch import Elasticsearch

postgres_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'user': 'admin',
    'password': 'admin'
}



conn = psycopg2.connect(
    host=postgres_config['host'],
    port=postgres_config['port'],
    database=postgres_config['database'],
    user=postgres_config['user'],
    password=postgres_config['password']
)

es = Elasticsearch(
    hosts=['http://localhost:9200'], 
    timeout=30, 
)


def fetch_data_from_postgres(table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return [dict(zip(columns, row)) for row in data]

class_materials_data = fetch_data_from_postgres("class_materials")


for material in class_materials_data:
    document = {
        "class_id": material["class_id"],
        "file": material["file"]
    }
    es.index(index="class_materials_index",id=material["id"], body=document)