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


def gen_group_course_f():
    file = open("group_course.sql", "w")
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )
    cursor = connection.cursor()

    query = 'INSERT INTO group_course(course_id, group_id, special) VALUES\n'
    cursor.execute(f'SELECT id FROM groups')
    groups_ids = cursor.fetchall()
    for group in groups_ids:        
        course_numbers = [random.randint(1, 40) for _ in range(random.randint(6, 13))]
        special = random.choice([True, False])
        for course in course_numbers:
            query += f"({course}, {group[0]}, {special}),\n"
    query = query[:-2]

    cursor.execute(query)
    connection.commit()
    connection.close()
    file.write(query)
    file.close()

def gen_classes_f():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )

    cur = connection.cursor()

    cur.execute("SELECT id FROM courses")

    course_ids = cur.fetchall()
    

    insert_statements = 'INSERT INTO classes(type_id, title, equipment, course_id) VALUES \n'
    for course_id in course_ids:
        for i in range(1, 17):
        
            practice_data = (1, f"Практика {i}", f"{random.choice([True, False])}", course_id[0])
            lecture_data = (2, f"Лекция {i}", f"{random.choice([True, False])}", course_id[0])

            insert_statements += f"{practice_data},\n"
            insert_statements += f"{lecture_data},\n"

    insert_statements = insert_statements[:-2]
    cur.execute(insert_statements)
    connection.commit()
    connection.close()

    with open('classes.sql', 'w') as file:
        file.write(insert_statements)


def gen_materials_f():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydb",
        user="admin",
        password="admin"
    )

    cur = connection.cursor()
    cur.execute("SELECT id FROM classes");
    classes = cur.fetchall()
    
    materials = [
    'программирование', 'Java', 'Python', 'C++', 'алгоритм', 'интернет', 
    'база данных', 'SQL', 'система контроля версий', 'Git', 'веб-разработка', 
    'JavaScript', 'HTML', 'CSS', 'Backend', 'Frontend', 'API', 'фреймворк', 
    'объектно-ориентированное программирование', 'ООП', 'структуры данных', 
    'интерпретатор', 'компилятор', 'операционная система', 'Linux', 'Windows', 
    'MacOS', 'сети', 'антивирус', 'хакер', 'безопасность', 'SSL', 'криптография', 
    'двухфакторная аутентификация', 'облако', 'блокчейн', 'контейнеризация', 
    'Docker', 'виртуализация', 'веб-сервер', 'бэкенд', 'фронтенд', 'мобильное приложение', 
    'Android', 'iOS', 'агил', 'SCRUM', 'DevOps', 'баг', 'тестирование', 
    'сборка', 'отладка', 'интеграция', 'инфраструктура как код', 'CI/CD', 
    'непрерывная поставка', 'сервер', 'клиент', 'софтверные требования', 
    'документация', 'проектирование', 'архитектура', 'база данных', 'NoSQL', 
    'масштабируемость', 'оптимизация', 'производительность', 'обратная совместимость', 
    'фронтенд разработка', 'бэкенд разработка', 'веб-дизайн', 'реляционная база данных', 
    'транзакция', 'хранилище данных', 'сессия', 'веб-сокет', 'RESTful API', 
    'микросервисы', 'серверный рендеринг', 'одностраничное приложение', 'искусственный интеллект', 
    'машинное обучение', 'нейронная сеть', 'биг-дата', 'анализ данных', 'распределенные системы',
    'веб-разработчик', 'тестировщик', 'DevOps инженер', 'системный администратор', 'программист', 
    'кодирование', 'инженерия программного обеспечения', 'бэкенд-разработчик', 'фронтенд-разработчик', 
    'дизайн интерфейса', 'пользовательский опыт', 'верстка', 'рефакторинг', 'вёрстка', 'распределенные базы данных', 
    'облачные вычисления', 'компьютерная безопасность', 'цифровая подпись', 'шифрование', 'блокчейн технологии', 
    'умный договор', 'экосистема', 'подпись', 'интернет вещей', 'IoT', 'скопление данных', 'резервное копирование', 
    'виртуальная среда', 'облачные сервисы', 'эксплуатация', 'реинжиниринг', 'код', 'заголовок',
    'цикл разработки', 'телефонное приложение', 'протокол', 'локальная сеть', 'UI/UX', 'интерфейс', 
    'техническая поддержка', 'реализация', 'робототехника', 'моделирование', 'подпись', 'API-интерфейс', 
    'архитектура программного обеспечения', 'веб-сервис', 'многопользовательский доступ', 'администрирование сети', 
    'резервная копия', 'удаленный сервер', 'системная архитектура', 'виртуальная машина'
    ]

    file = open('materials.sql', 'w')

    query = 'INSERT INTO class_materials(class_id, file) VALUES\n'
    for clas in classes:
        classes_id = clas[0]
        for _ in range(1, random.randint(2, 3)):
            text = ' '.join([random.choice(materials) for _ in range(random.randint(3, 12))])
            query += f"({classes_id}, '{text}'),\n"
    query = query[:-2]
    cur.execute(query)
    connection.commit()
    connection.close()

    file.write(query)
    file.close()


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

    start_date = datetime.strptime("2023-09-01", '%Y-%m-%d')
    end_date = datetime.strptime("2023-12-24", '%Y-%m-%d')
    delta = (end_date - start_date).days // 32
    dates = []
    for i in range(32):
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
        cursor.execute(query)
        file.write(query + '\n')

    connection.commit()
    connection.close()
    file.close()

gen_students_f()
print('Внесены данные в таблицу students')
gen_group_course_f()
print('Внесены данные в таблицу group_courses')
gen_classes_f()
print('Внесены данные в таблицу classes')
gen_materials_f()
print('Внесены данные в таблицу materials')
gen_scheldue_f()
print('Внесены данные в таблицу scheldue')
gen_attendances_f()
print('Внесены данные в таблицу attendances')