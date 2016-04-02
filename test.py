from data import *
from flask import Flask, render_template, flash, request, url_for, redirect
#from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = ""
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            #flash(attempted_username) # debugging only
            #flash(attempted_password)
            # do this with data.py functions later
            if attempted_username == "student" and attempted_password == "password":
                return redirect(url_for('student'))
            else:
                flash("Incorrect username/password.")
        return render_template("index.html", error = error)
    except Exception as e:
        #flash(e) #debugging only
        return render_template("index.html", error = error)
    return render_template("index.html")

@app.route('/student/')
def student():
    flash("for the love of lenin, please do log in and session stuff")
    return render_template("student.html")

@app.route('/teacher/')
def teacher():
    return render_template("teacher.html")

@app.route('/admin/')
def admin():
    return "this is the admin page boiiii"

@app.errorhandler(404)
def four_zero_four(e):
    return render_template("404.html")

@app.errorhandler(500)
def five_hundred(e):
    return render_template("500.html", error = e)

#app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = "totally secret, probably should be hashed"

# debugging only
if __name__ == "__main__":
    app.run(host='0.0.0.0')


