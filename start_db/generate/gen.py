import os

from post_gen.gen_students import gen_students
from post_gen.gen_group_course import gen_group_course
from post_gen.gen_classes import gen_classes
from post_gen.gen_materials import gen_materials
from post_gen.gen_sheldue import gen_scheldue
from post_gen.gen_attendances import gen_attendances

gen_students()
print('Внесены данные в таблицу students')
gen_group_course()
print('Внесены данные в таблицу group_courses')
gen_classes()
print('Внесены данные в таблицу classes')
gen_materials()
print('Внесены данные в таблицу materials')
gen_scheldue()
print('Внесены данные в таблицу scheldue')
gen_attendances()
print('Внесены данные в таблицу attendances')
