from datetime import datetime, timedelta

year = 2023

filename = "partition_instructions.sql"
with open(filename, "w") as file:
    for week_num in range(1, 53):
        start_date = datetime.strptime(f"{year}-W{week_num:02d}-0", "%Y-W%U-%w") + timedelta(days=1) 
        end_date = start_date + timedelta(days=7) 

        instruction = f"CREATE TABLE attendances_y{year}_w{week_num} PARTITION OF attendances\n"
        instruction += f"    FOR VALUES FROM ('{start_date.strftime('%Y-%m-%d')}') TO ('{end_date.strftime('%Y-%m-%d')}');\n"

        file.write(instruction)

print(f"Файл {filename} успешно создан.")