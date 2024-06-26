-- Active: 1698141293582@@127.0.0.1@5432@mydb
--tables

CREATE TABLE universities(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE institutes(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    university_id BIGINT NOT NULL
);

CREATE TABLE departments(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    institute_id BIGINT NOT NULL
);

CREATE TABLE specialities(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL
);

CREATE TABLE department_speciality(
    id SERIAL PRIMARY KEY,
    department_id BIGINT NOT NULL,
    speciality_id BIGINT NOT NULL
);

CREATE TABLE groups(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    speciality_id BIGINT NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE courses(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    department_id BIGINT NOT NULL,
    department_tag BOOLEAN NOT NULL
);

CREATE TABLE group_course(
    id SERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    special BOOLEAN NOT NULL
);

CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    fullname TEXT NOT NULL,
    code VARCHAR(6) NOT NULL UNIQUE,
    group_id BIGINT NOT NULL
);

CREATE TABLE class_type(
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE TABLE classes(
    id SERIAL PRIMARY KEY,
    type_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    equipment TEXT NOT NULL,
    course_id BIGINT NOT NULL
);

CREATE TABLE class_materials(
    id SERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL,
    file TEXT NOT NULL
);

CREATE TABLE schedule(
    id SERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL,
    group_id BIGINT NOT NULL,
    date DATE NOT NULL,
    pair_number INTEGER NOT NULL
);


CREATE TABLE attendances(
    id SERIAL,
    schedule_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    attended BOOLEAN NOT NULL,
    schedule_date DATE NOT NULL,
    CONSTRAINT attendances_pkey PRIMARY KEY (id, schedule_date)
) PARTITION BY RANGE (schedule_date);




ALTER TABLE
    department_speciality ADD CONSTRAINT department_speciality_speciality_id_foreign FOREIGN KEY(speciality_id) REFERENCES specialities(id);
ALTER TABLE
    group_course ADD CONSTRAINT group_course_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    groups ADD CONSTRAINT groups_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_student_id_foreign FOREIGN KEY(student_id) REFERENCES students(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_schedule_id_foreign FOREIGN KEY(schedule_id) REFERENCES schedule(id);
ALTER TABLE
    departments ADD CONSTRAINT departments_institute_id_foreign FOREIGN KEY(institute_id) REFERENCES institutes(id);
ALTER TABLE
    department_speciality ADD CONSTRAINT department_speciality_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    groups ADD CONSTRAINT groups_speciality_id_foreign FOREIGN KEY(speciality_id) REFERENCES specialities(id);
ALTER TABLE
    group_course ADD CONSTRAINT group_course_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);
ALTER TABLE
    classes ADD CONSTRAINT classes_type_id_foreign FOREIGN KEY(type_id) REFERENCES class_type(id);
ALTER TABLE
    students ADD CONSTRAINT students_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);
ALTER TABLE
    schedule ADD CONSTRAINT schedule_class_id_foreign FOREIGN KEY(class_id) REFERENCES classes(id);
ALTER TABLE
    courses ADD CONSTRAINT courses_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    classes ADD CONSTRAINT classes_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    class_materials ADD CONSTRAINT class_materials_class_id_foreign FOREIGN KEY(class_id) REFERENCES classes(id);
ALTER TABLE
    institutes ADD CONSTRAINT institutes_university_id_foreign FOREIGN KEY(university_id) REFERENCES universities(id);
ALTER TABLE
    schedule ADD CONSTRAINT schedule_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);

CREATE OR REPLACE PROCEDURE insert_attendances(student_i BIGINT, schedule_i BIGINT, attended BOOLEAN) LANGUAGE plpgsql 
AS $$
DECLARE
    _date TIMESTAMP WITHOUT TIME ZONE;
BEGIN
_date := (SELECT date FROM schedule WHERE id = schedule_i);
INSERT INTO attendances(student_id, schedule_id, attended, schedule_date)
    VALUES (student_i, schedule_i, attended, _date);
END
$$;

ALTER TABLE schedule REPLICA IDENTITY FULL;
ALTER TABLE departments REPLICA IDENTITY FULL;
ALTER TABLE courses REPLICA IDENTITY FULL;
ALTER TABLE institutes REPLICA IDENTITY FULL;
ALTER TABLE attendances REPLICA IDENTITY FULL;
ALTER TABLE students REPLICA IDENTITY FULL;
ALTER TABLE specialities REPLICA IDENTITY FULL;
ALTER TABLE group_course REPLICA IDENTITY FULL;
ALTER TABLE department_speciality REPLICA IDENTITY FULL;
ALTER TABLE groups REPLICA IDENTITY FULL;
ALTER TABLE classes REPLICA IDENTITY FULL;
ALTER TABLE class_materials REPLICA IDENTITY FULL;
ALTER TABLE universities REPLICA IDENTITY FULL;




CREATE TABLE attendances_y2023_w1 PARTITION OF attendances
    FOR VALUES FROM ('2023-01-02') TO ('2023-01-09');
CREATE TABLE attendances_y2023_w2 PARTITION OF attendances
    FOR VALUES FROM ('2023-01-09') TO ('2023-01-16');
CREATE TABLE attendances_y2023_w3 PARTITION OF attendances
    FOR VALUES FROM ('2023-01-16') TO ('2023-01-23');
CREATE TABLE attendances_y2023_w4 PARTITION OF attendances
    FOR VALUES FROM ('2023-01-23') TO ('2023-01-30');
CREATE TABLE attendances_y2023_w5 PARTITION OF attendances
    FOR VALUES FROM ('2023-01-30') TO ('2023-02-06');
CREATE TABLE attendances_y2023_w6 PARTITION OF attendances
    FOR VALUES FROM ('2023-02-06') TO ('2023-02-13');
CREATE TABLE attendances_y2023_w7 PARTITION OF attendances
    FOR VALUES FROM ('2023-02-13') TO ('2023-02-20');
CREATE TABLE attendances_y2023_w8 PARTITION OF attendances
    FOR VALUES FROM ('2023-02-20') TO ('2023-02-27');
CREATE TABLE attendances_y2023_w9 PARTITION OF attendances
    FOR VALUES FROM ('2023-02-27') TO ('2023-03-06');
CREATE TABLE attendances_y2023_w10 PARTITION OF attendances
    FOR VALUES FROM ('2023-03-06') TO ('2023-03-13');
CREATE TABLE attendances_y2023_w11 PARTITION OF attendances
    FOR VALUES FROM ('2023-03-13') TO ('2023-03-20');
CREATE TABLE attendances_y2023_w12 PARTITION OF attendances
    FOR VALUES FROM ('2023-03-20') TO ('2023-03-27');
CREATE TABLE attendances_y2023_w13 PARTITION OF attendances
    FOR VALUES FROM ('2023-03-27') TO ('2023-04-03');
CREATE TABLE attendances_y2023_w14 PARTITION OF attendances
    FOR VALUES FROM ('2023-04-03') TO ('2023-04-10');
CREATE TABLE attendances_y2023_w15 PARTITION OF attendances
    FOR VALUES FROM ('2023-04-10') TO ('2023-04-17');
CREATE TABLE attendances_y2023_w16 PARTITION OF attendances
    FOR VALUES FROM ('2023-04-17') TO ('2023-04-24');
CREATE TABLE attendances_y2023_w17 PARTITION OF attendances
    FOR VALUES FROM ('2023-04-24') TO ('2023-05-01');
CREATE TABLE attendances_y2023_w18 PARTITION OF attendances
    FOR VALUES FROM ('2023-05-01') TO ('2023-05-08');
CREATE TABLE attendances_y2023_w19 PARTITION OF attendances
    FOR VALUES FROM ('2023-05-08') TO ('2023-05-15');
CREATE TABLE attendances_y2023_w20 PARTITION OF attendances
    FOR VALUES FROM ('2023-05-15') TO ('2023-05-22');
CREATE TABLE attendances_y2023_w21 PARTITION OF attendances
    FOR VALUES FROM ('2023-05-22') TO ('2023-05-29');
CREATE TABLE attendances_y2023_w22 PARTITION OF attendances
    FOR VALUES FROM ('2023-05-29') TO ('2023-06-05');
CREATE TABLE attendances_y2023_w23 PARTITION OF attendances
    FOR VALUES FROM ('2023-06-05') TO ('2023-06-12');
CREATE TABLE attendances_y2023_w24 PARTITION OF attendances
    FOR VALUES FROM ('2023-06-12') TO ('2023-06-19');
CREATE TABLE attendances_y2023_w25 PARTITION OF attendances
    FOR VALUES FROM ('2023-06-19') TO ('2023-06-26');
CREATE TABLE attendances_y2023_w26 PARTITION OF attendances
    FOR VALUES FROM ('2023-06-26') TO ('2023-07-03');
CREATE TABLE attendances_y2023_w27 PARTITION OF attendances
    FOR VALUES FROM ('2023-07-03') TO ('2023-07-10');
CREATE TABLE attendances_y2023_w28 PARTITION OF attendances
    FOR VALUES FROM ('2023-07-10') TO ('2023-07-17');
CREATE TABLE attendances_y2023_w29 PARTITION OF attendances
    FOR VALUES FROM ('2023-07-17') TO ('2023-07-24');
CREATE TABLE attendances_y2023_w30 PARTITION OF attendances
    FOR VALUES FROM ('2023-07-24') TO ('2023-07-31');
CREATE TABLE attendances_y2023_w31 PARTITION OF attendances
    FOR VALUES FROM ('2023-07-31') TO ('2023-08-07');
CREATE TABLE attendances_y2023_w32 PARTITION OF attendances
    FOR VALUES FROM ('2023-08-07') TO ('2023-08-14');
CREATE TABLE attendances_y2023_w33 PARTITION OF attendances
    FOR VALUES FROM ('2023-08-14') TO ('2023-08-21');
CREATE TABLE attendances_y2023_w34 PARTITION OF attendances
    FOR VALUES FROM ('2023-08-21') TO ('2023-08-28');
CREATE TABLE attendances_y2023_w35 PARTITION OF attendances
    FOR VALUES FROM ('2023-08-28') TO ('2023-09-04');
CREATE TABLE attendances_y2023_w36 PARTITION OF attendances
    FOR VALUES FROM ('2023-09-04') TO ('2023-09-11');
CREATE TABLE attendances_y2023_w37 PARTITION OF attendances
    FOR VALUES FROM ('2023-09-11') TO ('2023-09-18');
CREATE TABLE attendances_y2023_w38 PARTITION OF attendances
    FOR VALUES FROM ('2023-09-18') TO ('2023-09-25');
CREATE TABLE attendances_y2023_w39 PARTITION OF attendances
    FOR VALUES FROM ('2023-09-25') TO ('2023-10-02');
CREATE TABLE attendances_y2023_w40 PARTITION OF attendances
    FOR VALUES FROM ('2023-10-02') TO ('2023-10-09');
CREATE TABLE attendances_y2023_w41 PARTITION OF attendances
    FOR VALUES FROM ('2023-10-09') TO ('2023-10-16');
CREATE TABLE attendances_y2023_w42 PARTITION OF attendances
    FOR VALUES FROM ('2023-10-16') TO ('2023-10-23');
CREATE TABLE attendances_y2023_w43 PARTITION OF attendances
    FOR VALUES FROM ('2023-10-23') TO ('2023-10-30');
CREATE TABLE attendances_y2023_w44 PARTITION OF attendances
    FOR VALUES FROM ('2023-10-30') TO ('2023-11-06');
CREATE TABLE attendances_y2023_w45 PARTITION OF attendances
    FOR VALUES FROM ('2023-11-06') TO ('2023-11-13');
CREATE TABLE attendances_y2023_w46 PARTITION OF attendances
    FOR VALUES FROM ('2023-11-13') TO ('2023-11-20');
CREATE TABLE attendances_y2023_w47 PARTITION OF attendances
    FOR VALUES FROM ('2023-11-20') TO ('2023-11-27');
CREATE TABLE attendances_y2023_w48 PARTITION OF attendances
    FOR VALUES FROM ('2023-11-27') TO ('2023-12-04');
CREATE TABLE attendances_y2023_w49 PARTITION OF attendances
    FOR VALUES FROM ('2023-12-04') TO ('2023-12-11');
CREATE TABLE attendances_y2023_w50 PARTITION OF attendances
    FOR VALUES FROM ('2023-12-11') TO ('2023-12-18');
CREATE TABLE attendances_y2023_w51 PARTITION OF attendances
    FOR VALUES FROM ('2023-12-18') TO ('2023-12-25');
CREATE TABLE attendances_y2023_w52 PARTITION OF attendances
    FOR VALUES FROM ('2023-12-25') TO ('2024-01-01');
