# print("Hello World!")

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/form')
# def form():
#     return render_template("form.html")

@app.route('/student')
def student():
    return render_template("student.html")

@app.route("/cca")
def cca():
    return render_template("cca.html")

@app.route('/login')
def login():
    return render_template("login.html")
    
app.run("0.0.0.0")