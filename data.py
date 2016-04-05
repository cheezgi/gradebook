import gc
import sqlite3

#ugh
classes_connection = sqlite3.connect('db/classes.db')
students_connection = sqlite3.connect('db/student.db')
users_connection = sqlite3.connect('db/users.db')
grades_connection = sqlite3.connect('db/grades.db')
teachers_connection = sqlite3.connect('db/teachers.db')
attendance_connection = sqlite3.connect('db/attendance.db')

classes = classes_connection.cursor()
students = students_connection.cursor()
users = users_connection.cursor()
grades = grades_connection.cursor()
teachers = teachers_connection.cursor()
attendance = attendance_connection.cursor()

# TODO: add other functions for user data manipulation
# TODO: possible import users/students from another database

def newdb():
    students.execute('''CREATE TABLE IF NOT EXISTS student (
            id INTEGER NOT NULL,
            class TEXT NOT NULL,
            grade INTEGER NOT NULL,
            teacher TEXT NOT NULL,
            transcript_file TEXT NOT NULL);''')
    grades.execute('''CREATE TABLE IF NOT EXISTS grades (
            id INTEGER NOT NULL,
            class TEXT NOT NULL,
            category TEXT NOT NULL,
            item TEXT NOT NULL,
            grade INTEGER NOT NULL,
            outOf INTEGER NOT NULL,
            date TEXT NOT NULL,
            weight INTEGER NOT NULL);''')
    users.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL);''')
    classes.execute('''CREATE TABLE IF NOT EXISTS classes (
            id INTEGER UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL);''')

def register(username, password):
    # relies on falseness of []
    if not users.execute("SELECT * FROM users WHERE username=?", (username,)).fetchall():
        users.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        users_connection.commit()
        return True
    else:
        return False

def get_pass(username):
    #no duplicate usernames, so indexing is OK
    return users.execute('SELECT * FROM users WHERE username=?', (username,)).fetchall()[0][1]
