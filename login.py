import hashlib
import sqlite3

classes = sqlite3.connect('classes.db').cursor()
classes.execute('''CREATE TABLE IF NOT EXISTS classes (
        id INTEGER NOT NULL,
        class TEXT NOT NULL,
        grade INTEGER NOT NULL,
        teacher TEXT NOT NULL)''')

users = sqlite3.connect('users.db').cursor()
users.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL)''')

def StudentLogin(username, password):
    user = hashlib.sha512(str(username)).hexdigest()
    pwd = hashlib.sha512(str(password)).hexdigest()

    userpass = users.execute('SELECT * FROM users WHERE username=?', (user,))

    if user == pwd:
        #something?

def StudentRegister(idnumber, password, classes):
