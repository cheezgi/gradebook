from data import *
from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/student/')
def student(): #this is really cool
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

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run()

