# test comment
from flask import Flask, render_template, request
import csv

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
                              "method": "post"},
                           
                          form_data = {
                              "description": "",
                              "start_date": "",
                              "end_date": ""
                          },
                           
                          type = "new"
                          )

@app.route("/confirm_activity", methods = ["POST", "GET"])
def confirm_activity():
    if "confirm" in request.args:
        return render_template("add_activity.html",
                              
                               form_meta = {
                                  "action": "/register_activity?registered",
                                  "method": "post"},
                               
                               form_data = {
                                   "start_date": request.form["start_date"],
                                   "end_date": request.form["end_date"],
                                   "description": request.form["description"]
                              },
                               
                              type = "confirm"
                              )

@app.route("/register_activity", methods=["POST", "GET"])
def register_activity():

    # jun xiang my brother
    
    if "registered" in request.args:
        return render_template("add_activity.html",

                               form_data = {
                                   "start_date": request.form["start_date"],
                                   "end_date": request.form["end_date"],
                                   "description": request.form["description"]
                               },

                               type="registered"
                              )


@app.route("/view_students")
def view_students():

    #jun xiang my brother
    #part of student class? -edwin
    #------- test data start
    data = []
    with open("test_data.csv", "r") as f:
        reader = csv.DictReader(f)
        for record in reader:
            record["View more/Edit"] = record["name"]
            data.append(record)
    #-------- test data end
    
    return render_template("view_students.html",
                           record_data = data
                          )


@app.route("/search_record", methods=["GET", "POST"])
def search_record():
    
    if "student_name" in request.args:

        #jun xiang my brother
        #------- test data start
        test_record_data = {
            "name": "Lebron James",
            "class": "0623",
            "cca": "Dance Club",
            "activity": "4 rings via"
        }
        
        record_data_name = test_record_data["name"]
        #-------- test data end
        
        return render_template("search_record.html",

                               form_data = {
                                   "student_name": request.args["student_name"]},

                               record_data = test_record_data,
                               record_data_name = record_data_name, #for the "edit" buttons
                               


    else:
        return render_template("search_record.html",
                               form_meta = {
                                   "action": "/search_record?student_name",
                                   "method": "GET"},
                               
                               form_data = {
                                   "student_name": ""},
    
                               type = "new"
                              )

@app.route("/cca_membership", methods=["POST", "GET"])
def edit_cca_membership():
    #backend retrieve activity info
    #student_name = 
    #student_activity = 
    return render_template("edit_data.html",
                          form_meta = {
                              "action": "/confirm_edit?cca",
                              "method": "GET"},
                          form_data = {
                              "student_name": "student_name",
                              "student_activity": "student_activity"},
                          type="cca")
    
@app.route("/activity_participation", methods=["POST", "GET"])
def edit_activity_participation():
    #backend retrieve activity info
    #student_name = 
    #student_activity = 
    return render_template("edit_data.html",
                          form_meta = {
                              "action": "/confirm_edit?activity",
                              "method": "GET"},
                          form_data = {
                              "student_name": "student_name",
                              "student_activity": "student_activity"},
                           type="activity")

@app.route("/confirm_edit", methods=["POST"])
def confirm_edit():
    if "activity" in request.args():
        form_data = {
            "student_name": request.form["student_name"],
            "student_activity": request.form["student_activity"]
        }
        return render_template("edit_data.html",
                              form_meta = {
                                  "action": "/register_data?activity",
                                  "method": "POST"},
                              form_data=form_data,
                              type="confirm")
        
    elif "cca" in request.args():
        form_data = {
            "student_name": request.form["student_name"],
            "student_cca": request.form["student_cca"]
        }
        return render_template("edit_data.html",
                              form_meta = {
                                  "action": "/register_data?cca",
                                  "method": "POST"},
                              form_data=form_data,
                              type="confirm")

@app.route("/register_data", methods=["POST"])
def registered_edit():
    if "cca" in request.args():
        data = {
            "student_name": request.form["student_name"],
            "student_cca": request.form["student_cca"]
        }
        
    elif "activity" in request.args():
        data = {
            "student_name": request.form["student_name"],
            "student_activity": request.form["student_activity"]
        }
    #backend: update data into db
    
    return render_template("edit_data.html",
                              form_data = data,
                              type="registered")
app.run("0.0.0.0")
