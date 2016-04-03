import hashlib
import sqlite3

classes = sqlite3.connect('db/classes.db').cursor()
students = sqlite3.connect('db/student.db').cursor()
users = sqlite3.connect('db/sers.db').cursor()
grades = sqlite3.connect('db/grades.db').cursor()
teachers = sqlite3.connect('db/teachers.db').cursor()

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

def connect():
    return classes, students, users, grades, teachers

