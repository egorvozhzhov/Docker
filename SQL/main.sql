--tables
CREATE TABLE departments(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    institute_id BIGINT NOT NULL
);

CREATE TABLE courses(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    scheduled_hours INTEGER NOT NULL,
    special_department BOOLEAN NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE institutes(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    university_id BIGINT NOT NULL
);

drop TABLE attendances CASCADE;
CREATE TABLE attendances(
    id SERIAL,
    class_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    class_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT attendances_pkey PRIMARY KEY (id, class_date)
) PARTITION BY RANGE (class_date);

CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    fio TEXT NOT NULL,
    code VARCHAR(6) NOT NULL UNIQUE,
    group_id BIGINT NOT NULL
);

CREATE TABLE specialities(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE student_course(
    id SERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL
);

drop table "groups" CASCADE;
CREATE TABLE groups(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    speciality_id BIGINT NOT NULL
);

CREATE TABLE classes(
    id SERIAL PRIMARY KEY,
    type VARCHAR(255) CHECK (type IN('lection', 'practice')) NOT NULL,
    date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    description TEXT NOT NULL,
    equipment TEXT NOT NULL,
    course_id BIGINT NOT NULL
);

CREATE TABLE universities(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    inn BIGINT NOT NULL
);

--foreign keys
ALTER TABLE
    student_course ADD CONSTRAINT student_course_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    student_course ADD CONSTRAINT student_course_student_id_foreign FOREIGN KEY(student_id) REFERENCES students(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_student_id_foreign FOREIGN KEY(student_id) REFERENCES students(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_class_id_foreign FOREIGN KEY(class_id) REFERENCES classes(id);
ALTER TABLE
    groups ADD CONSTRAINT groups_speciality_id_foreign FOREIGN KEY(speciality_id) REFERENCES specialities(id);
ALTER TABLE
    students ADD CONSTRAINT students_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);
ALTER TABLE
    courses ADD CONSTRAINT courses_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    classes ADD CONSTRAINT classes_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    specialities ADD CONSTRAINT specialities_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    institutes ADD CONSTRAINT institutes_university_id_foreign FOREIGN KEY(university_id) REFERENCES universities(id);
ALTER TABLE
    departments ADD CONSTRAINT departments_institute_id_foreign FOREIGN KEY(institute_id) REFERENCES institutes(id);

CREATE OR REPLACE PROCEDURE insert_attendances(student_i BIGINT, schedule_i BIGINT, attended BOOLEAN) LANGUAGE plpgsql 
AS $$
DECLARE
    _date TIMESTAMP WITHOUT TIME ZONE;
BEGIN
_date := (SELECT date_time FROM schedule WHERE id = schedule_i);
INSERT INTO attendances(student_id, schedule_id, attended, schedule_date)
    VALUES (student_i, schedule_i, attended, _date);
END
$$;


DROP PROCEDURE insert_attendances(student_i BIGINT, class_i BIGINT);

CREATE TABLE attendances_y2022_w1 PARTITION OF attendances
    FOR VALUES FROM ('2022-01-03') TO ('2022-01-10');
CREATE TABLE attendances_y2022_w2 PARTITION OF attendances
    FOR VALUES FROM ('2022-01-10') TO ('2022-01-17');
CREATE TABLE attendances_y2022_w3 PARTITION OF attendances
    FOR VALUES FROM ('2022-01-17') TO ('2022-01-24');
CREATE TABLE attendances_y2022_w4 PARTITION OF attendances
    FOR VALUES FROM ('2022-01-24') TO ('2022-01-31');
CREATE TABLE attendances_y2022_w5 PARTITION OF attendances
    FOR VALUES FROM ('2022-01-31') TO ('2022-02-07');
CREATE TABLE attendances_y2022_w6 PARTITION OF attendances
    FOR VALUES FROM ('2022-02-07') TO ('2022-02-14');
CREATE TABLE attendances_y2022_w7 PARTITION OF attendances
    FOR VALUES FROM ('2022-02-14') TO ('2022-02-21');
CREATE TABLE attendances_y2022_w8 PARTITION OF attendances
    FOR VALUES FROM ('2022-02-21') TO ('2022-02-28');
CREATE TABLE attendances_y2022_w9 PARTITION OF attendances
    FOR VALUES FROM ('2022-02-28') TO ('2022-03-07');
CREATE TABLE attendances_y2022_w10 PARTITION OF attendances
    FOR VALUES FROM ('2022-03-07') TO ('2022-03-14');
CREATE TABLE attendances_y2022_w11 PARTITION OF attendances
    FOR VALUES FROM ('2022-03-14') TO ('2022-03-21');
CREATE TABLE attendances_y2022_w12 PARTITION OF attendances
    FOR VALUES FROM ('2022-03-21') TO ('2022-03-28');
CREATE TABLE attendances_y2022_w13 PARTITION OF attendances
    FOR VALUES FROM ('2022-03-28') TO ('2022-04-04');
CREATE TABLE attendances_y2022_w14 PARTITION OF attendances
    FOR VALUES FROM ('2022-04-04') TO ('2022-04-11');
CREATE TABLE attendances_y2022_w15 PARTITION OF attendances
    FOR VALUES FROM ('2022-04-11') TO ('2022-04-18');
CREATE TABLE attendances_y2022_w16 PARTITION OF attendances
    FOR VALUES FROM ('2022-04-18') TO ('2022-04-25');
CREATE TABLE attendances_y2022_w17 PARTITION OF attendances
    FOR VALUES FROM ('2022-04-25') TO ('2022-05-02');
CREATE TABLE attendances_y2022_w18 PARTITION OF attendances
    FOR VALUES FROM ('2022-05-02') TO ('2022-05-09');
CREATE TABLE attendances_y2022_w19 PARTITION OF attendances
    FOR VALUES FROM ('2022-05-09') TO ('2022-05-16');
CREATE TABLE attendances_y2022_w20 PARTITION OF attendances
    FOR VALUES FROM ('2022-05-16') TO ('2022-05-23');
CREATE TABLE attendances_y2022_w21 PARTITION OF attendances
    FOR VALUES FROM ('2022-05-23') TO ('2022-05-30');
CREATE TABLE attendances_y2022_w22 PARTITION OF attendances
    FOR VALUES FROM ('2022-05-30') TO ('2022-06-06');
CREATE TABLE attendances_y2022_w23 PARTITION OF attendances
    FOR VALUES FROM ('2022-06-06') TO ('2022-06-13');
CREATE TABLE attendances_y2022_w24 PARTITION OF attendances
    FOR VALUES FROM ('2022-06-13') TO ('2022-06-20');
CREATE TABLE attendances_y2022_w25 PARTITION OF attendances
    FOR VALUES FROM ('2022-06-20') TO ('2022-06-27');
CREATE TABLE attendances_y2022_w26 PARTITION OF attendances
    FOR VALUES FROM ('2022-06-27') TO ('2022-07-04');
CREATE TABLE attendances_y2022_w27 PARTITION OF attendances
    FOR VALUES FROM ('2022-07-04') TO ('2022-07-11');
CREATE TABLE attendances_y2022_w28 PARTITION OF attendances
    FOR VALUES FROM ('2022-07-11') TO ('2022-07-18');
CREATE TABLE attendances_y2022_w29 PARTITION OF attendances
    FOR VALUES FROM ('2022-07-18') TO ('2022-07-25');
CREATE TABLE attendances_y2022_w30 PARTITION OF attendances
    FOR VALUES FROM ('2022-07-25') TO ('2022-08-01');
CREATE TABLE attendances_y2022_w31 PARTITION OF attendances
    FOR VALUES FROM ('2022-08-01') TO ('2022-08-08');
CREATE TABLE attendances_y2022_w32 PARTITION OF attendances
    FOR VALUES FROM ('2022-08-08') TO ('2022-08-15');
CREATE TABLE attendances_y2022_w33 PARTITION OF attendances
    FOR VALUES FROM ('2022-08-15') TO ('2022-08-22');
CREATE TABLE attendances_y2022_w34 PARTITION OF attendances
    FOR VALUES FROM ('2022-08-22') TO ('2022-08-29');
CREATE TABLE attendances_y2022_w35 PARTITION OF attendances
    FOR VALUES FROM ('2022-08-29') TO ('2022-09-05');
CREATE TABLE attendances_y2022_w36 PARTITION OF attendances
    FOR VALUES FROM ('2022-09-05') TO ('2022-09-12');
CREATE TABLE attendances_y2022_w37 PARTITION OF attendances
    FOR VALUES FROM ('2022-09-12') TO ('2022-09-19');
CREATE TABLE attendances_y2022_w38 PARTITION OF attendances
    FOR VALUES FROM ('2022-09-19') TO ('2022-09-26');
CREATE TABLE attendances_y2022_w39 PARTITION OF attendances
    FOR VALUES FROM ('2022-09-26') TO ('2022-10-03');
CREATE TABLE attendances_y2022_w40 PARTITION OF attendances
    FOR VALUES FROM ('2022-10-03') TO ('2022-10-10');
CREATE TABLE attendances_y2022_w41 PARTITION OF attendances
    FOR VALUES FROM ('2022-10-10') TO ('2022-10-17');
CREATE TABLE attendances_y2022_w42 PARTITION OF attendances
    FOR VALUES FROM ('2022-10-17') TO ('2022-10-24');
CREATE TABLE attendances_y2022_w43 PARTITION OF attendances
    FOR VALUES FROM ('2022-10-24') TO ('2022-10-31');
CREATE TABLE attendances_y2022_w44 PARTITION OF attendances
    FOR VALUES FROM ('2022-10-31') TO ('2022-11-07');
CREATE TABLE attendances_y2022_w45 PARTITION OF attendances
    FOR VALUES FROM ('2022-11-07') TO ('2022-11-14');
CREATE TABLE attendances_y2022_w46 PARTITION OF attendances
    FOR VALUES FROM ('2022-11-14') TO ('2022-11-21');
CREATE TABLE attendances_y2022_w47 PARTITION OF attendances
    FOR VALUES FROM ('2022-11-21') TO ('2022-11-28');
CREATE TABLE attendances_y2022_w48 PARTITION OF attendances
    FOR VALUES FROM ('2022-11-28') TO ('2022-12-05');
CREATE TABLE attendances_y2022_w49 PARTITION OF attendances
    FOR VALUES FROM ('2022-12-05') TO ('2022-12-12');
CREATE TABLE attendances_y2022_w50 PARTITION OF attendances
    FOR VALUES FROM ('2022-12-12') TO ('2022-12-19');
CREATE TABLE attendances_y2022_w51 PARTITION OF attendances
    FOR VALUES FROM ('2022-12-19') TO ('2022-12-26');
CREATE TABLE attendances_y2022_w52 PARTITION OF attendances
    FOR VALUES FROM ('2022-12-26') TO ('2023-01-02');

--tests
INSERT INTO universities(title, inn)
VALUES ('МИРЭА', 353454354);


INSERT INTO institutes(title, university_id)
VALUES ('ИКБ', 1), ('ИИТ', 1);

INSERT INTO departments(code, title, institute_id)
VALUES ('КБ-3','Рарзработка безопасных решений', 1), ('КБ-14','Цифровые технологии обработки данных', 1), ('КБ-9','Предметно-ориентированные информационные системы', 1), ('КППИ','Кафедра практической и прикладной информатики', 2), ('КВТ','Кафедра вычислительной техники', 2), ('КПИС','Кафедра копоративных информационнох систем', 2);

INSERT INTO specialities(code, title, department_id)
VALUES ('09.03.02','Информационные системы и технологии', 1),('09.03.02','Информационные системы и технологии', 2),('09.03.02','Информационные системы и технологии', 3), ('09.03.02','Информационные системы и технологии', 4),
('10.03.01','Информационная безопаность', 1), ('09.03.01','Информатика и вычислительная техника', 4), ('09.03.01','Информатика и вычислительная техника', 5),
('09.03.04','Программная инженерия', 5), ('09.03.04','Программная инженерия', 6);

INSERT INTO groups(title, speciality_id)
VALUES ('БСБО-01-20', 1), ('БСБО-02-20', 1), ('БСБО-03-20', 1), ('БСБО-17-20', 1), ('БСБО-04-20', 2), ('БСБО-05-20', 2), ('БСБО-12-20', 3), ('ИКРО-01-20', 4), 
('БИСО-01-20', 5), ('ВАНК-01-20', 6), ('ВАНК-02-20', 6), ('ВАНК-03-20', 7), ('ВАНК-04-20', 7), ('БИБУ-01-20', 8), ('БОКИ-01-20', 9);

INSERT INTO students(fio,code, group_id)
VALUES ('Иванов Иван Иванович', '20M200',1);

INSERT INTO courses(title, description, scheduled_hours, special_department, department_id)
VALUES ('Разработка чего то умного','Ебашьте и все получится',120,TRUE,1);

INSERT INTO classes(type,date, description, equipment, course_id)
VALUES ('lection', '2023-10-22', 'Делали что то умное', 'Подушка для жопы', 1);

CALL insert_attendances(1, 1);

/*
CREATE TABLE IF NOT EXISTS lections
(
    id INT GENERATED ALWAYS AS IDENTITY,
    date_time DATE NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS students
(
    id INT GENERATED ALWAYS AS IDENTITY,
    code VARCHAR(7) NOT NULL,
    group_code VARCHAR(12) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS visits
(
    id INT GENERATED ALWAYS AS IDENTITY,
    lection_id int,
    student_id int,
    lection_date timestamp,
    PRIMARY KEY(id),
    CONSTRAINT fk_lection
      FOREIGN KEY(lection_id) 
    REFERENCES lections(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_student
      FOREIGN KEY(student_id) 
    REFERENCES students(id)
      ON DELETE CASCADE
);

--date
CREATE OR REPLACE FUNCTION trg_attendances_date() RETURNS trigger AS $att_date$
    BEGIN
        NEW.class_date := (SELECT date FROM classes WHERE id = NEW.class_id);
        RETURN NEW;
    END;
$att_date$ LANGUAGE plpgsql;

--partitions
CREATE OR REPLACE FUNCTION trg_attendances() RETURNS trigger AS $func$
DECLARE
    _tbl text;
    _rec_date date;
    _min_date date;
    _max_date date;
BEGIN
NEW.class_date := (SELECT date FROM classes WHERE id = NEW.class_id);
_tbl := to_char(NEW.class_date, '"visits_y"IYYY_"w"IW');
_rec_date := NEW.class_date::date;
_min_date := date_trunc('week', NEW.class_date)::date;
_max_date := date_trunc('week', NEW.class_date)::date + 7;

IF NOT EXISTS (
    SELECT 1
    FROM   pg_catalog.pg_class c
    JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE  n.nspname = 'public'
    AND    c.relname = _tbl
    AND    c.relkind = 'r') THEN
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF attendances
                        FOR VALUES FROM (''%L'') TO (''%L'');'
            , _tbl
            , to_char(_min_date, 'YYYY-MM-DD')
            , to_char(_max_date, 'YYYY-MM-DD'));
END IF;
RETURN NEW;
END
$func$ LANGUAGE plpgsql;
*/

SELECT * FROM classes WHERE course_id=10


SELECT * FROM schedule WHERE class_id = 318

SELECT COUNT(*) FROM students WHERE group_id=7

SELECT * FROM group_course WHERE course_id=15