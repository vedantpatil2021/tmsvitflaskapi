from application import app
from flask import request
from views import *

app.app_context().push()

@app.route('/')
def rootpage():
    return "Server initiated at Port=5000"

# Authentication

@app.route('/register/ZpRpkIdXrt',methods=['GET','POST'])
def register():
    return registration()

@app.route('/login',methods=['POST'])
def login():
    return loginUser()

@app.route('/logout',methods=["POST"])
def logout():
    return logout_user()

@app.route('/@me')
def get_current_user():
    return authenticate()

@app.route('/upload_userdata', methods=['POST'])
def uploadfile():
    return create_multiple_user()


# Dashboard
@app.route('/dashboard',methods=["GET"])
def dashboard():
    return dash()


# Timetable CRUD
@app.route('/tthistory',methods=["GET"])
def tthistory():
    return tt_history()


@app.route('/get_tt/<string:tt_id>',methods=["GET"])
def get_tt(tt_id):
    return get_particular_tt(tt_id)

@app.route('/get_specific_tt/<string:tt_id>',methods=["GET"])
def get_specific_tt(tt_id):
    return get_tt_details(tt_id)

@app.route('/delete_tt/<string:tt_id>',methods=["DELETE"])
def delete_tt(tt_id):
    return delete_particular_tt(tt_id)

@app.route('/update_tt/<string:tt_id>',methods=["POST"])
def update_tt(tt_id):
    return updatett(tt_id)

@app.route('/make_public/<string:tt_id>',methods=["POST"])
def make_public(tt_id):
    return check_public(tt_id)

@app.route('/resetttdata/<string:tt_id>',methods=["POST"])
def reset_data(tt_id):
    return makebacktonormal(tt_id)

@app.route('/public_tt',methods=["GET"])
def public_data():
    return get_public_data()


# Enrollement 
@app.route('/enroll',methods=["POST"])
def enroll():
    return enrollment()


@app.route('/get_enroll_data',methods=["GET"])
def get_enroll_data():
    return get_enrollment()


# Timetable Data
@app.route('/rooms',methods=["GET"])
def room():
    return rooms()

@app.route('/meeting_times',methods=["GET"])
def meetingtime():
    return meetingtimes()

@app.route('/instructors',methods=["GET"])
def instructor():
    return instructors()

@app.route('/departments',methods=["GET"])
def department():
    return departments()

@app.route('/courses',methods=["GET"])
def course():
    return courses()

@app.route('/sections',methods=["GET"])
def section():
    return sections()


# Test API Endpoint
@app.route('/test',methods=["GET"])
def test():
    return testview()
