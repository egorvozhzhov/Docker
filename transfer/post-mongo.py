import psycopg2
from pymongo import MongoClient

pg_connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydb",
    user="admin",
    password="admin"
)

mongo_client = MongoClient('mongodb://localhost:27017/', username='root', password='password', authSource='admin')
mongo_db = mongo_client["structure"]

def fetch_data_from_postgres(table_name):
    cursor = pg_connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return [dict(zip(columns, row)) for row in data]

universities_data = fetch_data_from_postgres("universities")
institutes_data = fetch_data_from_postgres("institutes")
departments_data = fetch_data_from_postgres("departments")

universities_with_institutes = []
for university in universities_data:
    university["institutes"] = [{"id": institute["id"], 
                                 "title": institute["title"]} 
                                 for institute in institutes_data if institute["university_id"] == university["id"]]
    universities_with_institutes.append(university)

for institute in institutes_data:
    institute_departments = [{"id": department["id"], 
                              "code": department["code"], 
                              "title": department["title"]} 
                              for department in departments_data if department["institute_id"] == institute["id"]]
    for university in universities_with_institutes:
        for u_institute in university["institutes"]:
            if u_institute["id"] == institute["id"]:
                u_institute["departments"] = institute_departments


mongo_db.universities.insert_many(universities_with_institutes)