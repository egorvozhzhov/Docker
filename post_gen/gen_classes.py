import psycopg2
import random

def gen_classes_f():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )

    cur = connection.cursor()

    practice_equipments = ["laptop", "projector", "whiteboard", "microscope", "camera", "tools", "sensors", "server"]
    lecture_equipments = ["projector", "whiteboard", "microphone", "speakers", "screen", "laptop", "tablet", "camera"]

    cur.execute("SELECT id FROM courses")

    course_ids = cur.fetchall()
    

    insert_statements = 'INSERT INTO classes(type_id, title, equipment, course_id) VALUES \n'
    for course_id in course_ids:
        for i in range(1, 9):
            l_eq = ' '.join([random.choice(practice_equipments) for _ in range(random.randint(1, 3))])
            p_eq = ' '.join([random.choice(lecture_equipments) for _ in range(random.randint(1, 3))])
            practice_data = (1, f"Практика {i}", p_eq, course_id[0])
            lecture_data = (2, f"Лекция {i}", l_eq, course_id[0])

            insert_statements += f"{practice_data},\n"
            insert_statements += f"{lecture_data},\n"

    insert_statements = insert_statements[:-2]
    cur.execute(insert_statements)
    connection.commit()
    connection.close()

    with open('classes.sql', 'w') as file:
        file.write(insert_statements)




