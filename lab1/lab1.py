from elasticsearch import Elasticsearch
import psycopg2
import redis

from neo4j import GraphDatabase


def start_lab1(phrase, start_date, end_date):
    results = find_mat(phrase)
    results = list(set(results))

    result2 = find_schedules_by_class_id(results)
    result2 = list(set(result2))

    res = get_schedule(results)
    ress = [i[0] for i in res]

    students = get_codes(result2, start_date, end_date, ress)
    final=[]

    for student in students:
        name, code = get_info(student[0])
        final.append([name, code, round(student[1], 2)])

    return final

    


def find_mat(phrase):
    es = Elasticsearch(
        hosts=['http://elasticsearch:9200'], 
        timeout=30,
    )
    query = {
        "size": 10000,
        "query": {
            "match_phrase": {
                "file": phrase
            }
        }
    }
    result = es.search(index='class_materials_index', body=query)

    class_ids = [hit['_source']['class_id'] for hit in result['hits']['hits']]

    return class_ids




def find_schedules_by_class_id(class_ids):
    uri = "bolt://neo4j:7687"
    data = []
    query = (
        "MATCH (c:Class {type: 'lection', id: $classId})<-[:HAS_CLASS]-(co:Course)<-[:STUDY_COURSE]-(g:Group)<-[:STUDY_IN]-(s:Student) "
        "RETURN DISTINCT s.id as student_id"
    )

    with GraphDatabase.driver(uri) as driver:
        for class_id in class_ids:
            with driver.session() as session:
                result = session.run(query, classId=class_id)
                for record in result:
                    data.append(record["student_id"])
                   

    return data

def get_schedule(class_ids):
    class_ids = str(class_ids)[1:-1]
    connection = psycopg2.connect(
        host="postgres",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute(f"""SELECT id FROM schedule WHERE class_id IN ({class_ids})""")
    result = cursor.fetchall()
    return result


def get_codes(students_ids, start_date, end_date, schedule_ids):
    stud = str(students_ids)[1:-1]
    schedules = str(schedule_ids)[1:-1]
    connection = psycopg2.connect(
        host="postgres",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()
    cursor.execute(f"""SELECT a.student_id AS student_id, COUNT(CASE WHEN a.attended THEN 1 END) * 100.0 / COUNT(*) AS attendance_percentage
                        FROM
                            attendances a
                        WHERE a.student_id IN ({stud}) AND a.schedule_id IN ({schedules})
                            AND a.schedule_date BETWEEN '{start_date}' AND '{end_date}'
                        GROUP BY
                            student_id
                        ORDER BY
                            attendance_percentage ASC
                        LIMIT 10;
                        """)
    result = cursor.fetchall()
    connection.close()
    return result


def get_info(student):
    r = redis.Redis(
        host='redis',
        port=6379,
        decode_responses=True
    )
    student_info = r.hget(student, "fullname")
    student_code = r.hget(student, "code")
    return [student_info, student_code]
  



