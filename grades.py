from data import *
from flask import Flask, render_template, flash, request, url_for, redirec
from passlib.hash import sha256_crypt
from wtforms import Form
#from werkzeug.contrib.fixers import ProxyFix #uncomment for gunicorn uwsgi

# todo: database searching for matched passwords
# todo: possible default password for new students
# todo: grades, schedule, transcript, attendance
# todo: possible automatic scheduling conflict resolving

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    try:
        if request.method == "POST":
            isTeacher = request.form['isteacher'] == "true" # yup.
            if not isTeacher:
                attempted_username = request.form['student_username']
                attempted_password = sha256_crypt.encrypt(request.form['student_password'])
                if attempted_username == "student" and attempted_password == "password":
                    return redirect(url_for('student'))
                else:
                    flash("Incorrect username/password, please try again.")
            else:
                attempted_username = request.form['teacher_username']
                attempted_password = rsha256_crypt.encrypt(request.form['teacher_password'])
                if attempted_username == "teacher" and attempted_password == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8":
                    return redirect(url_for('teacher'))
                else:
                    flash("Incorrect username/password, please try again.")
        elif request.method == "GET":
            isTeacher = True
        return render_template("index.html", error = error)
    except Exception as e:
        return render_template("index.html", error = error)
    return render_template("index.html")

@app.route('/student/')
def student():
    flash("for the love of lenin, please do log in and session stuff")
    return render_template("student.html")

@app.route('/teacher/')
def teacher():
    return render_template("teacher.html")

@app.route('/admin_login/', methods=["POST", "GET"])
def admin_login():
    try:
        if request.method == "POST":
            attempted_username = request.form['admin_username']
            attempted_password = sha256_crypt.encrypt(request.form['admin_password'])
            if attempted_username == "admin" and attempted_password == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8":
                return redirect(url_for('admin'))
            return render_template("admin_login.html")
    except Exception as e:
        return render_template("admin_login.html")
    return render_template("admin_login.html")

# a default password is likely to be used in the future
class RegisterStudents(Form):
    username = TextField('Username', [validators.Length(min = 5, max = 10)])
    email = TextField('Email Address', [validators.Length(min = 6, max = 50)])
    password = PasswordField('Password', [validators.Required(),
        validators.EqualTo('confirm', message = "Passwords must match")])
    confirm = PasswordFiled('Re-type Password')
    accept_tos = BooleanField('I am not a robot', [validators.Required()])

@app.route('/admin/', methods = ['POST', 'GET'])
def admin():
    try:
        form = RegisterStudents(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(form.password.data)
    except Exception as e:
        return str(e)
    classes, students, users, grades, teachers = data.connect()
    return render_template("admin.html")

@app.errorhandler(404)
def four_zero_four(e):
    return render_template("404.html")

@app.errorhandler(500)
def five_hundred(e):
    return render_template("500.html", error = e)

#app.wsgi_app = ProxyFix(app.wsgi_app) #uncomment for gunicorn uwsgi

app.secret_key = "totally secret, probably should be hashed"

# debugging only
if __name__ == "__main__":
    app.run(host='0.0.0.0')


