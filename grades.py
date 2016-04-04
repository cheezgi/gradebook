import data
from flask import Flask, render_template, flash, request, url_for, redirect, session, g
import gc
import os
from passlib.hash import sha256_crypt
from wtforms import Form, BooleanField, TextField, PasswordField, validators
#from werkzeug.contrib.fixers import ProxyFix #uncomment for gunicorn uwsgi

# TODO: database searching for matched passwords
# TODO: possible default password for new students
# TODO: grades, schedule, transcript, attendance
# TODO: possible automatic scheduling conflict resolving

#app callable, used in gunicorn -b 0.0.0.0:80 grades:app
app = Flask(__name__)

#index page
@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    try:
        if request.method == "POST":
            #derpy way of determining form name
            isTeacher = request.form['isteacher'] == "true" # yup.

            if not isTeacher:
                attempted_username = request.form['student_username']
                attempted_password = sha256_crypt.encrypt(request.form['student_password'])

                if attempted_username == "student" and attempted_password == u"5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8":
                    session['logged_in'] = True
                    return redirect(url_for('student'))
                else:
                    flash("Incorrect username/password, please try again.")
            else:
                attempted_username = request.form['teacher_username']
                attempted_password = sha256_crypt.encrypt(request.form['teacher_password'])

                if attempted_username == "teacher" and attempted_password == u"5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8":
                    session['logged_in'] = True
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
            if attempted_username == "admin" and attempted_password == u"5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8":
                return redirect(url_for('admin'))
            return render_template("admin_login.html")
    except Exception as e:
        return render_template("admin_login.html")
    return render_template("admin_login.html")

@app.route('/admin/', methods=["GET", "POST"])
def admin():
    try:
        if request.method == "POST":
            formName = request.form['form_name']
            if formName == "register":
                new_username = request.form['new_username']
                if data.register(new_username, sha256_crypt.encrypt(u"default")):
                    flash("User registered")
                else:
                    flash("Username taken")
            if formName == "databases":
                data.newdb()
                flash("Databases created.")
    except Exception as e:
        flash(str(e))
    return render_template('admin.html')

@app.errorhandler(404)
def four_oh_four(e):
    return render_template("404.html")

@app.errorhandler(500)
def five_hundred(e):
    return render_template("500.html", error = e)

@app.errorhandler(405)
def method_not_allowed(e):
    return "<h1 style='color:red;'>405 error &#9773;&#9773;&#9773;&#9773;&#9773;&#9773;&#9773;&#9773;</h1>"

#app.wsgi_app = ProxyFix(app.wsgi_app) #uncomment for gunicorn uwsgi

app.secret_key = os.urandom(24)

# debugging only
if __name__ == "__main__":
    app.run(host='0.0.0.0')


