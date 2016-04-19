import data
from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from functools import wraps
import gc
import os
from passlib.hash import sha256_crypt
#from werkzeug.contrib.fixers import ProxyFix #uncomment for gunicorn uwsgi

# TODO: database searching for matched passwords
# TODO: possible default password for new students
# TODO: grades, schedule, transcript, attendance
# TODO: possible automatic scheduling conflict resolving

#app callable, used in gunicorn -b 0.0.0.0:80 grades:app
app = Flask(__name__)

#doesn't work
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash("You must log in first.")
            return redirect(url_for('index'))
    return wrap

#index page
@app.route('/', methods=['GET', 'POST'])
def index():
    session['logged_in'] = False
    session['admin'] = False
    session['username'] = ""
    try:
        if request.method == "POST":
            #derpy way of determining form
            isTeacher = request.form['isteacher'] == "true" # yup.
            if not isTeacher:
                stud_username = request.form['student_username']
                stud_password = request.form['student_password']
                if sha256_crypt.verify(stud_password, data.get_pass(stud_username)):
                    session['logged_in'] = True
                    session['username'] = stud_username
                    return redirect(url_for('student'))
                else:
                    flash('Incorrect password/username, please try again')
            else:
                teach_username = request.form['teacher_username']
                teach_password = request.form['teacher_password']
                if sha256_crypt.verify(teach_password, data.get_pass(teach_username)):
                    session['logged_in'] = True
                    session['username'] = teach_username
                    return redirect(url_for('teacher'))
                else:
                    flash("Incorrect username/password, please try again.")
    except Exception as e:
        flash('That username does not exist, please try again. ' + str(e))
        return render_template("index.html")
    return render_template("index.html")

@login_required
@app.route('/student/')
def student():
    if not session['logged_in']:
        flash("You must be logged in to view this page.")
        return redirect(url_for('index'))
    return render_template("student.html")

@login_required
@app.route('/teacher/')
def teacher():
    if not session['logged_in']:
        flash('You must be logged in to view this page.')
        return redirect(url_for('index'))
    return render_template("teacher.html")

@app.route('/admin_login/', methods=["POST", "GET"])
def admin_login():
    session['admin'] = False
    try:
        if request.method == "POST":
            attempted_username = request.form['admin_username']
            attempted_password = sha256_crypt.encrypt(request.form['admin_password'])
            if sha256_crypt.verify('password', attempted_password) and attempted_username == "admin":
                session['logged_in'] = True
                session['admin'] = True
                return redirect(url_for('admin'))
            return render_template("admin_login.html")
    except Exception as e:
        return render_template("admin_login.html")
    return render_template("admin_login.html")

@login_required
@app.route('/admin/', methods=["GET", "POST"])
def admin():
    if not session['admin']:
        flash("You do not have rights to enter the admin page. This incedent will be reported.")
        #not really :D
        return redirect(url_for('index'))
    try:
        if request.method == "POST":
            formName = request.form['form_name']
            if formName == "register":
                new_username = request.form['new_username']
                if data.register(new_username, sha256_crypt.encrypt('password')):
                    flash("User registered")
                else:
                    flash("Username taken")
            if formName == "databases":
                data.newdb()
                flash("Databases created.")
            if formName == "logout":
                session['admin'] = False
                session['logged_in'] = False
                flash("Logged out.")
                return redirect(url_for('index'))
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
    app.run(host='0.0.0.0', debug=True)


