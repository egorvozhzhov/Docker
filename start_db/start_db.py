import psycopg2

query = ''
with open("start_db/main2.sql") as file:
    query = file.read()

connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="mydb",
    user="admin",
    password="admin"
)

cursor = connection.cursor()
cursor.execute(query)
connection.commit()
connection.close()
print('Создана схема, заполнены данные для университета, институтов, кафедр, специальностей, групп, курсов. Созданы партиции и хранимая процедура')