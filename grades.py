import data
from flask import Flask, render_template, flash, request, url_for, redirect, session, g, send_from_directory
from functools import wraps
import gc
import os
from passlib.hash import sha256_crypt
from subprocess import call
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
            #silly way to determine which form user is using
            isTeacher = request.form['isteacher'] == "true"
            if not isTeacher:
                stud_username = request.form['student_username']
                stud_password = request.form['student_password']
                #really slow
                if sha256_crypt.verify(stud_password, data.get_pass(stud_username)):
                    #make sure user is not a teacher, aka a student
                    if not data.check_if_teacher(stud_username):
                        session['logged_in'] = True
                        session['username'] = stud_username
                        return redirect(url_for('student'))
                    else:
                        #only if user is not a teacher
                        flash('Incorrect login')
                else:
                    flash('Incorrect password/username, please try again')
            else:
                teach_username = request.form['teacher_username']
                teach_password = request.form['teacher_password']
                if sha256_crypt.verify(teach_password, data.get_pass(teach_username)):
                    if data.check_if_teacher(teach_username):
                        session['logged_in'] = True
                        session['username'] = teach_username
                        return redirect(url_for('teacher'))
                    else:
                        flash('Incorrect login')
                else:
                    flash("Incorrect username/password, please try again.")
    except Exception as e:
        flash('That username does not exist, please try again.')
    return render_template("index.html")

@login_required #supposedly
@app.route('/student/', methods=["POST", "GET"])
def student():
    #login_required wrap doesn't work and session is encrypted anyway
    if not session['logged_in']:
        flash("You must be logged in to view this page.")
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            if request.form['logout'] == 'logout':
                session['logged_in'] = False
                flash('You have been logged out.')
                return redirect(url_for('index'))
        return render_template("student.html")

@login_required
@app.route('/teacher/')
def teacher():
    if not session['logged_in']:
        flash('You must be logged in to view this page.')
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            if request.form['logout'] == 'logout':
                session['logged_in'] = False
                flash('You have been logged out.')
                return redirect(url_for('index'))
        return render_template("teacher.html")

@app.route('/admin_login/', methods=["POST", "GET"])
def admin_login():
    session['admin'] = False
    try:
        if request.method == "POST":
            attempted_username = request.form['admin_username']
            attempted_password = request.form['admin_password']
            if sha256_crypt.verify(attempted_password, data.get_pass(attempted_username)):
                if data.check_if_admin(attempted_username):
                    session['logged_in'] = True
                    session['admin'] = True
                    session['username'] = attempted_username
                    return redirect(url_for('admin'))
                else:
                    flash('You do not have admin privileges.')
            else:
                flash('Incorrect credentials. This incedent will be logged.')
            return redirect(url_for('index'))
    except Exception as e:
        flash(e)
        return redirect(url_for('index'))
    return render_template('admin_login.html')

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
                new_id = request.form['new_id']
                try: #why would I do this
                    is_teacher = bool(request.form['is_teacher'])
                except Exception as e:
                    is_teacher = False
                try:
                    is_admin = bool(request.form['is_admin'])
                except Exception as e:
                    is_admin = False
                if data.register(new_username, sha256_crypt.encrypt('password'), new_id, is_admin, is_teacher):
                    flash("User registered")
                else:
                    flash("Username taken")
            if formName == "databases":
                data.newdb()
                flash("Databases created.")
            if formName == "logout":
                session['admin'] = False
                session['logged_in'] = False
                flash("Logged out")
                return redirect(url_for('index'))
            if formName == "admin_pass":
                username = session['username']
                new_pass = request.form['admin_new_pass']
                new_pass2 = request.form['admin_new_pass2']
                old_pass = request.form['admin_old_pass']
                if sha256_crypt.verify(old_pass, data.get_pass(username)):
                    if new_pass == new_pass2:
                        data.change_pass(username, sha256_crypt.encrypt(new_pass.encode('utf-8')))
                        flash('Your password has been changed.')
                    else:
                        flash('Old password is incorrect.')
                else:
                    flash('Passwords do not match.')
            if formName == "remove":
                username = request.form['rm_username']
                user_id = request.form['user_id']
                if data.remove(username, user_id):
                    flash("User successfully removed.")
                else:
                    flash("User does not exist.")
            if formName == "admin_pass":
                username = request.form['user_username']
                password = request.form['user_password']
                data.change_pass(username, sha256_crypt.encrypt(password.encode('utf-8')))
                flash("Password has been changed.")
            #don't really know if I want this
            if formName == "shutdown":
                call(["sudo", "pkill", "gunicorn"])
                flash("Server has been shut down.")
    except Exception as e:
        raise(e)
    return render_template('admin.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html", error = e)

@app.errorhandler(405)
def method_not_allowed(e):
    return "<h1 style='color:red;'>&#9773; 405 error: method not allowed &#9773;"

#app.wsgi_app = ProxyFix(app.wsgi_app) #uncomment for gunicorn uwsgi

#probably good enough...
app.secret_key = os.urandom(24)

# debugging only
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


