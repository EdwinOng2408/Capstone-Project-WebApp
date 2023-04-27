# test comment
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_cca", methods=["POST", "GET"])
def add_cca():
    return render_template("add_cca.html",
                           form_meta = {
                              "action": "/confirm_cca?confirm",
                              "method": "post"},
                           
                           form_data = {
                               "cca_name": "",
                               "cca_type": ""},
                           
                           type = "new"
                          )

@app.route("/confirm_cca", methods=["POST", "GET"])
def confirm_cca():
    if "confirm" in request.args:
        return render_template("add_cca.html",
                               form_meta = {
                                  "action": "/register_cca?registered",
                                  "method": "post"},
                               
                               form_data = {
                                   "cca_name": request.form["cca_name"],
                                   "cca_type": request.form["cca_type"]},
                               
                               type = "confirm" #to render confirm page
                              )

@app.route("/register_cca", methods=["POST", "GET"])
def register_cca():
    if "registered" in request.args:

        #jun xiang my brother
        
        return render_template("add_cca.html",
                               form_data = {
                                   "cca_name": request.form["cca_name"],
                                   "cca_type": request.form["cca_type"]},

                               type = "registered"
                              )
        
@app.route("/add_activity", methods=["POST", "GET"])
def add_activity():
    return render_template("add_activity.html",
                           
                          form_meta = {
                              "action": "/confirm_activity?confirm",
                              "methods": "POST"},
                           
                          form_data = {
                              "decription": "",
                              "start_date": "",
                              "end_date": ""
                          },
                           
                          type = "add"
                          )

@app.route("/confirm_activity", methods = ["POST", "GET"])
def confirm_activity():
    if "confirm" in request.args():
        return render_template("add_activity.html",
                              
                              form_meta = {
                                  "action": "/register_cca?registered",
                                  "method": "POST"},

                              form_data = {
                                   "start_date": request.form["start_date"],
                                   "end_date": request.form["end_date"],
                                    "description": request.form["description"]
                              }
                               
                              type = "confirm"
                              )

@app.route("/register_activity", methods=["POST", "GET"])
def register_activity():
    if "registered" in request.args():
        return render_template("add_activity.html",

                               form_data = {
                                   "start_date": request.form["start_date"],
                                   "end_date": request.form["end_date"],
                                   "description": request.form["description"]
                               },

                               type="registered"
                              )
                               
app.run("0.0.0.0")
