import random
from datetime import datetime, timedelta
import psycopg2


def gen_scheldue_f():


    connection = psycopg2.connect(
        host='localhost', 
        port='5432', 
        dbname='mydb', 
        user='admin', 
        password='admin'
    )
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM courses")
    courses = [i[0] for i in cursor.fetchall()]

    start_date = datetime.strptime("2022-02-07", '%Y-%m-%d')
    end_date = datetime.strptime("2022-06-11", '%Y-%m-%d')
    delta = (end_date - start_date).days // 16
    dates = []
    for i in range(16):
        date = start_date + timedelta(days=i * delta)
        dates.append(date)


    query = f"INSERT INTO schedule (class_id, group_id, date, pair_number) VALUES\n"

    for course_id in courses:
        cursor.execute(f"SELECT id FROM classes WHERE course_id = {course_id}")
        class_records = cursor.fetchall()
        classes = [cl[0] for cl in class_records]
        for i, cl in enumerate(classes):
            cursor.execute(f"SELECT g.id FROM classes cl INNER JOIN courses co ON cl.course_id = co.id INNER JOIN group_course gc ON gc.course_id = co.id INNER JOIN groups g ON gc.group_id = g.id WHERE cl.id = {cl}")
            group_records = cursor.fetchall()
            groups = [gr[0] for gr in group_records]
            for gr in groups:
                pair = random.randint(1,6)
                query += f"({cl}, {gr}, '{dates[i]}', {pair}),\n"
    query = query[:-2]
    with open("schedule.sql", "w") as file:
        file.write(query+ ';')
    cursor.execute(query)
    connection.commit()
    connection.close()

gen_scheldue_f()