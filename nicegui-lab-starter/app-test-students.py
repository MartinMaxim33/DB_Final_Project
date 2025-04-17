# Script to let us test the functionality of the user table.
# Can add a user, print them, read from CSV.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *
from nicegui import ui

# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def get_students():
    print("Executing SQL query")
    cur.execute("SELECT student_id, first_name, last_name, grad_year FROM students")
    rows = cur.fetchall()
    return rows

def get_courses():
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    print("Here are the courses:")
    return rows

def add_student(student_id, first_name, last_name, grad_year):
    print(student_id)
    cur.execute("INSERT INTO students (student_id, first_name, last_name, grad_year) VALUES (%s, %s, %s, %s)", [student_id, first_name, last_name, grad_year])
    conn.commit()  # mandatory to actually write the data to the db

def add_course(course_id, department, course_number, course_section, course_name, start_time, prof_name):
    print(course_id)
    cur.execute("INSERT INTO courses (course_id, department, course_number, course_section, course_name, start_time, prof_name) VALUES (?, ?, ?, ?, ?, ?, ?)", [course_id, department, course_number, course_section, course_name, start_time, prof_name])
    conn.commit()  # mandatory to actually write the data to the db
@ui.page('/')
def homepage():
    ui.label("Welcome to the homepage!")
    ui.link("Test Students", '/test_students')

@ui.page('/test_students')
def test_students():
    student_info = get_students()
    print(student_info)
    ui.table(rows=student_info)

    with ui.row().classes('items-center'):
        ui.label('Student ID:')
        student_id_box = ui.input()
    with ui.row().classes('items-center'):
        ui.label('First name:')
        first_name_box = ui.input()
    with ui.row().classes('items-center'):
        ui.label('Last name:')
        last_name_box = ui.input()
    with ui.row().classes('items-center'):
        ui.label('Gradation year:')
        grad_year_box = ui.input()

    ui.button('Add Student', on_click=lambda: add_student(student_id_box.value, first_name_box.value, last_name_box.value, grad_year_box.value))

ui.run(reload=False)


@ui.page('/test_courses')
def test_courses():
    course_info = get_courses()
    print(course_info)
    ui.table(rows=course_info)

    with ui.row().classes('items-center'):
        ui.label('ID:')
        course_id_box = ui.input()
    with ui.row().classes('items-center'):
        ui.label('Department:')
        department_box = ui.input()
    with ui.row().classes('items-center'):
        ui.label('Number:')
        number_box = ui.input()
    with ui.row().classes('items-center'):
            ui.label('Section:')
            section_box = ui.input()
    with ui.row().classes('items-center'):
            ui.label('Number:')
            number_box = ui.input()
    with ui.row().classes('items-center'):
                ui.label('Department:')
                department_box = ui.input()
    with ui.row().classes('items-center'):
                ui.label('Number:')
                number_box = ui.input()


    ui.button('Add Course', on_click=lambda: add_student(course_id_box.value, department_box.value, number_box.value))

ui.run(reload=False)
#cur.close()
#conn.close()