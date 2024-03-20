from flask import Flask, jsonify, request
from functools import wraps

from py2neo import Graph
import psycopg2
import redis
import json 

app = Flask(__name__)



@app.route('/', methods=['GET'])
def get_lab3():
    group = request.args.get('group')

    courses = get_volume_of_listened_hours(group)
    return jsonify({'group': group, "courses": courses}), 200


def get_volume_of_listened_hours(group:str) -> list:
    student_ids = get_students(group)
    if not student_ids:
        raise ValueError("Не найдены студенты")
    
    course_schedules = get_courses_schedules(group)
    if not course_schedules:
        raise ValueError("Не найдено расписание")
    
    courses = []
    for course_item in course_schedules:
        title = course_item[0]
        hours_info = get_students_hours(student_ids, course_item[1])
        planned = hours_info[0][2]
        students = []
        for item in hours_info:
            name, code = get_student_data(item[0])
            students.append({"fullname":name, "code":code, "valid_hours":item[1]})

        courses.append({"title":title, "planned_hours":planned, "students": students})

    return courses


def get_courses_schedules(group:str) -> dict:
    neo4j_graph = Graph("bolt://localhost:7687")
    query = f"""MATCH (group:Group {{title: "{group}"}})-[:STUDY_COURSE]->(course:Course {{department_tag: true}})-[:HAS_CLASS]->(class:Class)<-[:REFERS_TO_CLASS]-(sch:Schedule)
        RETURN course.title AS course_title, collect(sch.id) AS scheldue_ids"""
    result = neo4j_graph.run(query)

    return [[record["course_title"], record["scheldue_ids"]] for record in result]

def get_students(group:str) -> list:
    neo4j_graph = Graph("bolt://localhost:7687")
    query = f"""MATCH (g:Group {{title: "{group}"}})<-[:STUDY_IN]-(s:Student)
        RETURN s.id AS student_id"""
    result = neo4j_graph.run(query)

    return [record["student_id"] for record in result]



def get_students_hours(students:list, schedules:list) -> list:
    students_str = str(students)[1:-1]
    schedules_str = str(schedules)[1:-1]

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()

    cursor.execute(f"""SELECT student_id, COUNT(CASE WHEN attended THEN 1 END)*2 AS was, COUNT(*)*2 AS need
        FROM attendances
        WHERE student_id IN ({students_str}) AND schedule_id IN ({schedules_str})
        GROUP BY student_id""")
    
    result = cursor.fetchall()
    connection.close()
    return result



def get_student_data(key):
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    data = r.get(key)
    data = json.loads(data)
    fullname = data.get('fullname')
    code = data.get('code')
    return fullname, code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=13000)