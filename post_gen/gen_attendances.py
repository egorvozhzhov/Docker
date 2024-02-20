import random
import psycopg2

def gen_attendances_f():
    file = open("attendances.sql", "w")
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()

    cursor.execute(f'SELECT st.id, sc.id FROM schedule sc INNER JOIN groups g ON g.id = sc.group_id INNER JOIN students st on g.id = st.group_id;')
    mixes = cursor.fetchall()
    for mix in mixes:
        student_id = mix[0]
        schedule_id = mix[1]
        query = f"CALL insert_attendances({student_id}, {schedule_id}, {random.choice([True, False])});"
        #cursor.execute(query)
        file.write(query + '\n')

    #connection.commit()
    connection.close()
    file.close()

