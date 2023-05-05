# test comment
from flask import Flask, render_template, request
from storage import StudentData, StudentCCA, StudentActivity, CCACollection, ActivityCollection

#loading of collections
cca_table = CCACollection("capstone_project.db")
activity_table = ActivityCollection("capstone_project.db")
student_data = StudentData("capstone_project.db")
student_cca = StudentCCA("capstone_project.db")
student_activity = StudentActivity("capstone_project.db")

print(cca_table.find("Chinese Orchestra"))
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_cca", methods=["POST", "GET"])
def add_cca():
    return render_template("add_cca.html",
                           form_meta={
                               "action": "/confirm_cca?confirm",
                               "method": "post"
                           },
                           form_data={
                               "cca_name": "",
                               "cca_type": ""
                           },
                           type="new")


@app.route("/confirm_cca", methods=["POST", "GET"])
def confirm_cca():
    if "confirm" in request.args:

        return render_template(
            "add_cca.html",
            form_meta={
                "action": "/register_cca?registered",
                "method": "post"
            },
            form_data={
                "cca_name": request.form["cca_name"],
                "cca_type": request.form["cca_type"]
            },
            type="confirm"  #to render confirm page
        )


@app.route("/register_cca", methods=["POST", "GET"])
def register_cca():
    if "registered" in request.args:

        record = [request.form["cca_type"], request.form["cca_name"]]

        #backend
        #if cca already exists:
        #render template with type "error"
        #else:
        cca_table.insert(record)

        return render_template("add_cca.html",
                               form_data={
                                   "cca_name": request.form["cca_name"],
                                   "cca_type": request.form["cca_type"]
                               },
                               type="registered")


@app.route("/add_activity", methods=["POST", "GET"])
def add_activity():
    return render_template("add_activity.html",
                           form_meta={
                               "action": "/confirm_activity?confirm",
                               "method": "post"
                           },
                           form_data={
                               "activity_name": "",
                               "description": "",
                               "start_date": "",
                               "end_date": "",
                               "organizing_cca": ""
                           },
                           type="new")


@app.route("/confirm_activity", methods=["POST", "GET"])
def confirm_activity():
    if "confirm" in request.args:
        return render_template("add_activity.html",
                               form_meta={
                                   "action": "/register_activity?registered",
                                   "method": "post"
                               },
                               form_data={
                                   "activity_name":
                                   request.form["activity_name"],
                                   "start_date": request.form["start_date"],
                                   "end_date": request.form["end_date"],
                                   "description": request.form["description"],
                                   "organizing_cca":
                                   request.form["organizing_cca"]
                               },
                               type="confirm")


@app.route("/register_activity", methods=["POST", "GET"])
def register_activity():

    if "registered" in request.args:
        record = [
            request.form["activity_name"], request.form["start_date"],
            request.form["end_date"], request.form["description"],
            request.form["organizing_cca"]
        ]

        #backend
        #if activity already exists:
        #render template with type "error"
        #else:
        activity_table.insert(record)

        return render_template("add_activity.html",
                               form_data={
                                   "activity_name":
                                   request.form["activity_name"],
                                   "start_date": request.form["start_date"],
                                   "end_date": request.form["end_date"],
                                   "description": request.form["description"],
                                   "organizing_cca":
                                   request.form["organizing_cca"]
                               },
                               type="registered")


@app.route("/view_students")
def view_students():

    data = student_data.get_all()
    for record in data:
        record["View More/Edit"] = record["student_name"]
    return render_template("view_students.html", record_data=data)


@app.route("/search_record", methods=["GET", "POST"])
def search_record():

    if "student_name" in request.args:
        search_name = request.args["student_name"].replace("+", " ").replace("_", " ").upper()

        data = student_data.get_one(search_name)
        if data == []:
            type = "wrong_entry"
        else:
            type = "search"
        return render_template(
            "search_record.html",
            form_data={"student_name": search_name},
            record_data=data,
            record_data_name=search_name,  #for the "edit" buttons
            type=type)

    else:
        return render_template("search_record.html",
                               form_meta={
                                   "action": "/search_record",
                                   "method": "get"
                               },
                               form_data={"student_name": ""},
                               type="new")


@app.route("/cca_membership", methods=["POST", "GET"])
def edit_cca_membership():
    #backend retrieve activity info
    #student_name =
    #student_activity =

    action = request.args["action"]  #whether to insert or delete
    student_name = request.args["student_name"]

    return render_template("edit_record.html",
                           form_meta={
                               "action": f"/confirm_edit?cca&action={action}",
                               "method": "post"
                           },
                           form_data={
                               "student_name": student_name,
                               "student_cca": "",
                               "role": "Member"
                           },
                           type="new",
                           action=action)


@app.route("/activity_participation", methods=["POST", "GET"])
def edit_activity_participation():

    action = request.args["action"]  #whether to insert or delete
    student_name = request.args["student_name"]
    if action == "insert":
        form_data = {
            "student_name": student_name,
            "student_activity": "",
            "category": "",
            "role": "Participant",
            "award": "-",
            "hours": "-",
        }
    elif action == "delete":
        form_data = {"student_name": student_name, "student_activity": ""}

    return render_template("edit_record.html",
                           form_meta={
                               "action":
                               f"/confirm_edit?activity&action={action}",
                               "method": "post"
                           },
                           form_data=form_data,
                           type="new",
                           action=action)


@app.route("/confirm_edit", methods=["POST"])
def confirm_edit():

    action = request.args["action"]  #whether to insert or delete

    if "activity" in request.args:
        if action == "insert":
            form_data = {
                "student_name": request.form["student_name"],
                "student_activity": request.form["student_activity"],
                "category": request.form["category"],
                "role": request.form["role"],
                "award": request.form["award"],
                "hours": request.form["hours"]
            }
        else:
            form_data = {
                "student_name": request.form["student_name"],
                "student_activity": request.form["student_activity"]
            }

        return render_template("edit_record.html",
                               form_meta={
                                   "action":
                                   f"/register_data?activity&action={action}",
                                   "method": "POST"
                               },
                               form_data=form_data,
                               type="confirm",
                               action=action)

    elif "cca" in request.args:
        form_data = {
            "student_name": request.form["student_name"],
            "student_cca": request.form["student_cca"],
            "role": request.form["role"]
        }

        return render_template("edit_record.html",
                               form_meta={
                                   "action":
                                   f"/register_data?cca&action={action}",
                                   "method": "post"
                               },
                               form_data=form_data,
                               type="confirm",
                               action=action)


@app.route("/register_data", methods=["POST", "GET"])
def register_data():
    type = "registered"
    action = request.args["action"]

    if "cca" in request.args:
        data = {
            "student_name": request.form["student_name"],
            "student_cca": request.form["student_cca"],
            "role": request.form["role"]
        }
        if action == "delete":
            results = student_cca.delete(data["student_name"],
                                         data["student_cca"])
        elif action == "insert":
            results = student_cca.insert(data["student_name"],
                                         data["student_cca"], data["role"])

    elif "activity" in request.args:

        if action == "delete":
            data = {
                "student_name": request.form["student_name"],
                "student_activity": request.form["student_activity"]
            }
            results = student_activity.delete(data["student_name"],
                                              data["student_activity"])

        elif action == "insert":
            data = {
                "student_name": request.form["student_name"],
                "student_activity": request.form["student_activity"],
                "category": request.form["category"],
                "role": request.form["role"],
                "award": request.form["award"],
                "hours": request.form["hours"]
            }
            results = student_activity.insert(data["student_name"],
                                              data["student_activity"],
                                              data["category"], data["award"],
                                              data["hours"], data["role"])

    if results == False:
        type = "failed"
    return render_template("edit_record.html",
                           form_data=data,
                           type=type,
                           action=action)


app.run("0.0.0.0")
