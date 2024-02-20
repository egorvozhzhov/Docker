import psycopg2
from py2neo import Graph, Node, Relationship

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydb",
    user="admin",
    password="admin"
)

cursor = conn.cursor()
neo4j_graph = Graph("bolt://localhost:7687")

def fetch_data_from_postgres(table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return [dict(zip(columns, row)) for row in data]

#departments
departments = fetch_data_from_postgres("departments")

for department in departments:
    department_node = Node("Department", id=department["id"], code=department["code"], title=department["title"])
    neo4j_graph.create(department_node)

#specialities
specialities = fetch_data_from_postgres("specialities")

for speciality in specialities:
    speciality_node = Node("Speciality", id=speciality["id"], code=speciality["code"], title=speciality["title"])
    neo4j_graph.create(speciality_node)

#dep_spec
cursor.execute("SELECT department_id, speciality_id FROM department_speciality")
department_specialities = fetch_data_from_postgres("department_speciality")
for department_speciality in department_specialities:
    department_node = neo4j_graph.nodes.match("Department", id=department_speciality["department_id"]).first()
    speciality_node = neo4j_graph.nodes.match("Speciality", id=department_speciality["speciality_id"]).first()
    relationship = Relationship(department_node, "HAS_SPECIALITY", speciality_node)
    neo4j_graph.create(relationship)

#groups
groups = fetch_data_from_postgres("groups")
for group in groups:
    group_node = Node("Group", id=group["id"], title=group["title"])
    neo4j_graph.create(group_node)

    department_node = neo4j_graph.nodes.match("Department", id=group["department_id"]).first()
    speciality_node = neo4j_graph.nodes.match("Speciality", id=group["speciality_id"]).first()

    relationship_dep = Relationship(department_node, "OFFERS_GROUP", group_node)
    relationship_spec = Relationship(speciality_node, "HAS_GROUP", group_node)

    neo4j_graph.create(relationship_dep)
    neo4j_graph.create(relationship_spec)

#students
students = fetch_data_from_postgres("students")
for student in students:
    student_node = Node("Student", id=student["id"], code=student["code"])
    neo4j_graph.create(student_node)

    group_node = neo4j_graph.nodes.match("Group", id=student["group_id"]).first()
    relationship = Relationship(student_node, "STUDY_IN", group_node)
    neo4j_graph.create(relationship)

#courses
courses = fetch_data_from_postgres("courses")
for course in courses:
    course_node = Node("Course", id=course["id"], title=course["title"], department_tag= course["department_tag"])
    neo4j_graph.create(course_node)

    department_node = neo4j_graph.nodes.match("Department", id=course["department_id"]).first()
    relationship = Relationship(department_node, "HAS_COURSE", course_node)
    neo4j_graph.create(relationship)

#group_course

group_courses = fetch_data_from_postgres("group_course")
for group_course in group_courses:
    group_node = neo4j_graph.nodes.match("Group", id=group_course["group_id"]).first()
    course_node = neo4j_graph.nodes.match("Course", id=group_course["course_id"]).first()
    relationship = Relationship(group_node, "STUDY_COURSE", course_node, special=group_course["special"])
    neo4j_graph.create(relationship)

#classes
classes = fetch_data_from_postgres("classes")
for clas in classes:
    
    clas_node= Node("Class", id=clas["id"], type='practice' if clas["type_id"] == 1 else 'lection', title=clas["title"], equipment=clas["equipment"])
    neo4j_graph.create(clas_node)

    course_node = neo4j_graph.nodes.match("Course", id=clas["course_id"]).first()
    relationship = Relationship(course_node, "HAS_CLASS", clas_node)
    neo4j_graph.create(relationship)

#schedule
schedules = fetch_data_from_postgres("schedule")
for schedule in schedules:
    schedule_node = Node("Scheldue", id=schedule["id"], date=schedule["date"], pair_number=schedule["pair_number"])
    neo4j_graph.create(clas_node)

    clas_node = neo4j_graph.nodes.match("Class", id=schedule["class_id"]).first()
    relationship = Relationship(schedule_node, "REFERS_TO_CLASS", clas_node)
    neo4j_graph.create(relationship)

    group_node = neo4j_graph.nodes.match("Group", id=schedule["group_id"]).first()
    relationship = Relationship(schedule_node, "REFERS_TO_GROUP", group_node)
    neo4j_graph.create(relationship)
cursor.close()
conn.close()