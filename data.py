import gc
import sqlite3

#ugh
users_connection = sqlite3.connect('db/users.db')
students_connection = sqlite3.connect('db/students.db')
teachers_connection = sqlite3.connect('db/teachers.db')
grades_connection = sqlite3.connect('db/grades.db')
classes_connection = sqlite3.connect('db/classes.db')
attendance_connection = sqlite3.connect('db/attendance.db')
schedules_connection = sqlite3.connect('db/schedules.db')
#admins_connection = sqlite3.connect('db/admins.db')

users = users_connection.cursor()
students = students_connection.cursor()
teachers = teachers_connection.cursor()
grades = grades_connection.cursor()
classes = classes_connection.cursor()
attendance = attendance_connection.cursor()
schedules = schedules_connection.cursor()
#admins = admins_connection.cursor()

# TODO: add other functions for user data manipulation
# TODO: possible import users/students from another database

def newdb():
    users.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            id INTEGER UNIQUE NOT NULL,
            is_admin INTEGER NOT NULL,
            is_teacher INTEGER NOT NULL);''')
    users_connection.commit()
    students.execute('''CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            transcript_file TEXT UNIQUE NOT NULL);''')
    students_connection.commit()
    teachers.execute('''CREATE TABLE IF NOT EXISTS teachers (
            teacer_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL);''')
    teachers_connection.commit()
    #possibly still too big of a database
    grades.execute('''CREATE TABLE IF NOT EXISTS grades (
            student_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            item_name INTEGER NOT NULL,
            grade INTEGER NOT NULL,
            out_of INTEGER NOT NULL,
            date TEXT NOT NULL,
            weight INTEGER NOT NULL);''')
    grades_connection.commit()
    classes.execute('''CREATE TABLE IF NOT EXISTS classes (
            teacher_id INTEGER NOT NULL,
            class_name TEXT UNIQUE NOT NULL);''')
    classes_connection.commit()
    attendance.execute('''CREATE TABLE IF NOT EXISTS attendance (
            student_id INTEGER UNIQUE NOT NULL,
            date TEXT NOT NULL,
            type INTEGER NOT NULL);''')
    attendance_connection.commit()
    schedules.execute('''CREATE TABLE IF NOT EXISTS schedules (
            student_id INTEGER UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            teacher_id INTEGER NOT NULL);''')
    schedules_connection.commit()
#    admins.execute('''CREATE TABLE IF NOT EXISTS admins (
#            admin_username TEXT UNIQUE NOT NULL,
#            password TEXT NOT NULL,
#            name TEXT NOT NULL);''')
#    admins_connection.commit()

#user functions
def register(username, password, id, isadmin, isteacher):
    # relies on falseness of []
    if not users.execute("SELECT * FROM users WHERE username=?", (username,)).fetchall():
        users.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, password, id, isadmin, isteacher))
        users_connection.commit()
    else:
        return False
    return True

#def register_admin(username, password, name):
#    if not admins.execute("SELECT * FROM admins WHERE admin_username=?", (username,)).fetchall():
#        admins.execute("INSERT INTO admins VALUES (?, ?, ?)", (username, password, name))
#        admins_connection.commit()
#    else:
#        return False
#    return True
#
#def get_admin_pass(username):
#    try:
#        q = admins.execute('SELECT * FROM admins WHERE admin_username=?', (username,)).fetchall()[0][1]
#    except Exception as e:
#        return e
#    return q
#
#def change_admin_pass(new_pass, username, name):
#    try:
#        admins.execute("REPLACE INTO admins VALUES (?, ?, ?)", (username, new_pass, name))
#        admins_connection.commit()
#    except:
#        return False
#    return True
#
#def get_admin_name(username):
#    try:
#        q = admins.execute('SELECT name FROM admins WHERE admin_username=?', (username,)).fetchall()[0]
#        return q
#    except Exception as e:
#        return e

def get_pass(username):
    #no duplicate usernames, so indexing is OK
    try:
        q = users.execute('SELECT * FROM users WHERE username=?', (username,)).fetchall()[0][1]
    except Exception as e:
        return e
    return q

def check_if_teacher(username):
    try:
        q = users.execute('SELECT is_teacher FROM users WHERE username=?', (username,)).fetchall()[0][0]
    except Exception as e:
        return e
    return q

def get_student_grades(studentID):
    return users.execute('SELECT * FROM grades WHERE id=?', (studentID,)).fetchall()

def get_student_schedule(teacherID):
    return "this is not yet supported."

def update_grade(studentID, category, item, newGrade):
    return "this is not yet supported."
