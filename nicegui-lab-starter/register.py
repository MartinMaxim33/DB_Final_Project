# Script to let us register for classes.

import psycopg
from psycopg.rows import dict_row
from dbinfo import *


# Connect to an existing database
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")

# Open a cursor to perform database operations
cur = conn.cursor(row_factory=dict_row)

def list_students():
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    print("Here are the students:")
    for student in rows:
        print("ID:", student['student_id'], "Name:", student['first_name'], student['last_name'])

def list_courses():
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    print("Here are the courses:")
    for course in rows:
        print("ID:", course['course_id'], "Dept:", course['department'], "Number:", course['course_number'],
              "Section:", course['course_section'])

def list_student_schedule():
    list_students()

    chosen_student = int(input("Enter a student id: "))

    print("\nHere is their schedule:")
    cur.execute("SELECT department, course_number, course_section, course_name, start_time \
        FROM enroll NATURAL JOIN courses WHERE student_id=%s", [chosen_student])
    student_courses = cur.fetchall()
    print(student_courses)
    for course in student_courses:
        print(course['department'] + "-" + str(course['course_number']) + "-"
              + str(course['course_section']) + " at " + str(course['start_time']))

def list_course_roster():
    list_courses()

    chosen_student = int(input("Enter a course id: "))

    print("\nHere are the students:")
    cur.execute("SELECT first_name, last_name, grad_year \
        FROM enroll NATURAL JOIN students WHERE course_id=%s", [chosen_student])
    students = cur.fetchall()
    print(students)
    for stu in students:
        print(stu['first_name'], stu['last_name'], stu['grad_year'])

def enroll_student_in_course():
    # list all students
    # prompt for a student ID
    # list all courses
    # prompt for a course ID
    # add the student ID, course ID combination into the enroll table

    # Then add the ability to only pick courses that don't conflict in time
    # with a course they are already enrolled in.  Do this by changing your
    # query for listing all courses.  Hint: first write & test a query to get
    # all the course times the student is already enrolled in.

    list_students()

def main():
    print("Pick option:")
    print("1. List a student's schedule")
    print("2. List a class roster")
    print("3. Enroll a student in a course")
    print("4. Drop a student from a course")
    choice = int(input("Choose option: "))

    if choice == 1:
        list_student_schedule()
    elif choice == 2:
        list_course_roster()
    elif choice == 3:
        enroll_student_in_course()


main()