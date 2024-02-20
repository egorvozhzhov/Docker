from py2neo import Graph, NodeMatcher
from neo4j import GraphDatabase
import redis
import psycopg2
import json

group_name = "БСБО-03-20"


uri = "bolt://localhost:7687"
def get_schedule_for_group(group_name):
    query = (
        "MATCH (group:Group {title: $group_name})-[:STUDY_COURSE]->(course:Course {department_tag: true})-[:HAS_CLASS]->(class:Class)<-[:REFERS_TO_CLASS]-(sch:Scheldue) "
        "RETURN course.title AS course_title, collect(sch.id) AS scheldue_ids"
    )

    driver = GraphDatabase.driver(uri)
    with driver.session() as session:
        result = session.run(query, group_name=group_name)
        return result.data()


schedule_info = get_schedule_for_group(group_name)
print("Курс и соответствующие ему пары в расписании")
print(schedule_info)
print()
print()





def get_students_by_group_title(group_name):
    query = (
        "MATCH (group:Group {title: $group_name})<-[:STUDY_IN]-(student:Student)"
        "RETURN student.id AS student_id"
    )

    driver = GraphDatabase.driver(uri)
    with driver.session() as session:
        result = session.run(query, group_name=group_name)
        return result.data()



ids = get_students_by_group_title(group_name)


print(ids)
ids = [student['student_id'] for student in ids]
print(ids)
print()
print()

def get_info(student):
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    student_info = r.hget(student, "fullname")
    student_code = r.hget(student, "code")
    return [student_info, student_code]


def get_result(scheldue, students_id):
    stud = str(students_id)[1:-1]
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    print("Информация о посещенных/запланированных часах курсов (содержащих тег дисциплины кафедры):")
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("{:<60} {:<60} {:<10} {:<10} {:<10}".format('Название курса', 'ФИО студента', "Шифр студента", 'Посещено часов', 'Запланировано часов'))
    for i in range(len(scheldue)):
        schedules = str(schedule_info[i]['scheldue_ids'])[1:-1]

        cursor = connection.cursor()
        cursor.execute(f"""SELECT a.student_id AS student_id, COUNT(CASE WHEN a.attended THEN 1 END)*2 AS was, COUNT(*)*2 AS need
                            FROM
                                attendances a
                            WHERE a.student_id IN ({stud}) AND a.schedule_id IN ({schedules})
                            GROUP BY
                                student_id
                            """)
        result = cursor.fetchall()
       
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")

        for j in range(len(result)):
            
            st = get_info(result[j][0])
            fullname = st[0]
            code = st[1]
            
            
            print("{:<60} {:<60} {:<20} {:<10} {:<10}".format(scheldue[i]['course_title'], fullname, code, result[j][1], result[j][2]))

        
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
    connection.close()
    

get_result(schedule_info, ids)
