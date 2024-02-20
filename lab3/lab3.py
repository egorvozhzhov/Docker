from neo4j import GraphDatabase
import redis
import psycopg2
import json


def start_lab3(group_name):
    schedule_info = get_schedule_for_group(group_name)
    students, ids = get_students_by_group_title(group_name)
    formatted_dict = {person['id']: {'fullname': person['fullname'], 'code': person['code']} for person in students}
    final = get_result(schedule_info, ids, formatted_dict)
    return final



def get_schedule_for_group(group_name):
    uri = "bolt://neo4j:7687"
    query = (
        "MATCH (group:Group {title: $group_name})-[:STUDY_COURSE]->(course:Course {department_tag: true})-[:HAS_CLASS]->(class:Class)<-[:REFERS_TO_CLASS]-(sch:Scheldue) "
        "RETURN course.title AS course_title, collect(sch.id) AS scheldue_ids"
    )

    driver = GraphDatabase.driver(uri)
    with driver.session() as session:
        result = session.run(query, group_name=group_name)
        return result.data()




def get_students_by_group_title(group_title):
    r = redis.Redis(
        host='redis',
        port=6379,
        decode_responses=True
    )

    group_keys = r.keys(f"group:*:{group_title}")

    students = []
    student_ids = []
    for group_key in group_keys:
        for member in r.smembers(group_key):
            student_info = json.loads(member) 
            student_id = student_info['id']
            student_ids.append(student_id)
            students.append(student_info)

    return students, student_ids

def get_result(scheldue, students_id, formatted_dict):
    stud = str(students_id)[1:-1]
    connection = psycopg2.connect(
        host="postgres",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    final = []
    for i in range(len(scheldue)):
        schedules = str(scheldue[i]['scheldue_ids'])[1:-1]

        cursor = connection.cursor()
        cursor.execute(f"""SELECT a.student_id AS student_id, COUNT(CASE WHEN a.attended THEN 1 END)*2 AS was, COUNT(*)*2 AS need
                            FROM
                                attendances a
                            WHERE a.student_id IN ({stud}) AND a.schedule_id IN ({schedules})
                            GROUP BY
                                student_id
                            """)
        result = cursor.fetchall()

        for j in range(len(result)):
            
            st = formatted_dict[result[j][0]]
            fullname = st['fullname']
            code = st['code']
            final.append([scheldue[i]['course_title'], fullname, code, result[j][1], result[j][2]])
           

    connection.close()
    return final
    

