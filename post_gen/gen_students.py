import random
import string
import psycopg2

def gen_students_f():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    cursore = connection.cursor()
    query0 = "SELECT id FROM groups"
    cursore.execute(query0)
    group_records = cursore.fetchall()
    groups = [i[0] for i in group_records]
    

    lastnames = ["Кузнецов", "Бобров", "Началов", "Сидоров", "Баринов", "Александров", "Василин", "Карибов", "Петров", "Кузнецов", "Смирнов", "Васильев"]
    names = ["Максим", "Владислав", "Егор", "Григорий", "Михаил", "Евгений", "Виктор", "Степан", "Иван", "Петр", "Алексей", "Дмитрий", "Сергей"]
    patronymics = ["Александрович", "Григорьевич", "Викторович", "Михайлович", "Степанович", "Иванович", "Петрович", "Алексеевич", "Дмитриевич", "Сергеевич"]

    insert_query = "INSERT INTO students (fullname, code, group_id) VALUES\n"
    for _ in range(450):
        lastname = random.choice(lastnames)
        name = random.choice(names)
        patronymic = random.choice(patronymics)
        student_id = gen_id()
        group_id = random.choice(groups)

        insert_query += f"('{lastname} {name} {patronymic}', '{student_id}', {group_id}),\n"
    insert_query = insert_query[:-2]

    cursore.execute(insert_query)
    connection.commit()
    connection.close()


    filename = "students.sql"
    with open(filename, "w") as file:
        file.write(insert_query)

def gen_id():
    digits = string.digits
    alph = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЮЯ"

    student_id = ""
    for _ in range(6):
        symbol_type = random.randint(0, 1)
        if symbol_type == 0:
            symbol = random.choice(digits)
        else:
            symbol = random.choice(alph)

        student_id += symbol

    return student_id

