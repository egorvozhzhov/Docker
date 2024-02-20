import psycopg2
import redis
import json

postgres_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'user': 'admin',
    'password': 'admin'
}

redis_config = {
    'host': 'localhost',
    'port': 6379
}

conn = psycopg2.connect(
    host=postgres_config['host'],
    port=postgres_config['port'],
    database=postgres_config['database'],
    user=postgres_config['user'],
    password=postgres_config['password']
)


r = redis.Redis(
    host=redis_config['host'],
    port=redis_config['port'],
)

def fetch_data_from_postgres(table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return [dict(zip(columns, row)) for row in data]

students = fetch_data_from_postgres("students")

for student in students:
    id = student["id"]
    code = student["code"]
    fullname = student["fullname"]
    r.hset(id, mapping ={"fullname": fullname, "code":code})




cursor = conn.cursor()



cursor.execute("SELECT s.id, s.code, s.fullname, g.id, g.title FROM students s INNER JOIN groups g ON s.group_id = g.id")
rows = cursor.fetchall()

for row in rows:
    group_key = f"group:{row[3]}:{row[4]}"
    student_value = {"id": row[0], "code": row[1], "fullname": row[2]}
    serialized_student_value = json.dumps(student_value) 
    r.sadd(group_key, serialized_student_value)

cursor.close()
conn.close()