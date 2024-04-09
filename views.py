import json, os
from pymongo import MongoClient
from application import app
import random
import string
import pandas as pd
from models import *
from db import mongo
import random as rnd
from bson.objectid import ObjectId
from dotenv import load_dotenv
from bson import json_util
from pymongo import MongoClient
import datetime
import mimerender
from flask import request, jsonify,session
app.app_context().push()

load_dotenv()
mimerender.register_mime('pdf', ('application/pdf',))
mimerender = mimerender.FlaskMimeRender(global_charset='UTF-8')
client = MongoClient('mongodb://localhost:27017/')
mongodb = client['tmsvit']
collection = mongodb['tt_history']

# Authentication
def authenticate():
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()

    if not user_id:
        return jsonify({"error":"Unauthorized "}),401
    elif user_id:
        return jsonify({"message":"This is Dashboards","user_id":user.user_id,"username":user.username,"role":user.group,"university_id":user.university_id,"dept":user.dept})
    else:
        return jsonify({"error":"Something went wrong"}),404


def dash():
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()
    return jsonify({"message":"This is Dashboards","user_id":user.user_id,"username":user.username,"role":user.group})


def registration():

    form = request.form
    register = Authentication(
        username = form['username'],
        first_name = form['firstname'],
        last_name = form['lastname'],
        email = form['email'],
        group = "faculty",
        is_super_user = "yes",
        last_login = datetime.datetime.now(),
        date_joined = datetime.date.today(),
        dept = form['department']
    )
    
    register.set_password(form['password'])
    db.session.add(register)
    db.session.commit()
    return jsonify({"message":"Registration Successfull"})



def loginUser():
    if request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')
        auth  = Authentication.query.filter_by(username = username).first()

        if auth and auth.check_password(password):
            session['user_id'] = auth.user_id
            auth.last_login = datetime.datetime.now()
            db.session.commit()
            return jsonify({"id":auth.user_id,"email":auth.email,"role":auth.group,"name":auth.first_name + " " + auth.last_name}),200
        else:
            return jsonify({"message":"Login Error"}),401


    return jsonify({"message":"Username or Password Incorrect"})



def logout_user():
    session.pop('user_id')
    return jsonify({"message":"User Loged Out Successfully"}),200

def multiple_register(username,password,firstname,lastname,email,dept,university_id):
    
    register = Authentication(
        username = username,
        first_name = firstname,
        last_name = lastname,
        email = email,
        group = "student",
        is_super_user = "no",
        last_login = datetime.datetime.now(),
        date_joined = datetime.date.today(),
        dept = dept,
        university_id=university_id
    )
    register.set_password(password)
    db.session.add(register)
    db.session.commit()
    
    return jsonify({"message":"All Registration Successfull"})
    

def create_multiple_user():
    df = pd.read_excel("StudentData.xlsx")
    for index, row in df.iterrows():
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(12))
        username = df.at[index,'username']
        firstname = df.at[index,'firstname']
        lastname = df.at[index,'lastname']
        email = df.at[index,'email']
        dept = df.at[index,'dept']
        university_id = df.at[index,'universityid']
        multiple_register(username,password,firstname,lastname,email,dept,university_id)
    
    return jsonify({'data': "Done"})

######################### Timetable ###########################
def tt_history():
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()

    if user.group == "superadmin" or user.group == "ttfaculty":
        get_tt_history = TimetableHistory.query.all()
        result = []
        for get_tt_history in get_tt_history:
            result.append({"tt_id":get_tt_history.tt_id,"tt_dept":get_tt_history.tt_dept,"tt_name":get_tt_history.tt_name,"tt_unique_id":get_tt_history.tt_unique_id,"tt_status":get_tt_history.tt_status,"tt_date":get_tt_history.tt_date,"tt_time":get_tt_history.tt_time})

        return result
    elif user.group == "hod":
        get_tt = TimetableHistory.query.filter_by(tt_status = "AP")
        hodresult = []
        for get_tt in get_tt:
            hodresult.append({"tt_id":get_tt.tt_id,"tt_dept":get_tt.tt_dept,"tt_name":get_tt.tt_name,"tt_unique_id":get_tt.tt_unique_id,"tt_status":get_tt.tt_status,"tt_date":get_tt.tt_date,"tt_time":get_tt.tt_time})

        return hodresult
    else:
        return jsonify({"message":"Unauthorized Access"}), 401

def get_tt_details(tt_id):
    tt_data = TimetableHistory.query.filter_by(tt_id = tt_id).first()
    return jsonify({"tt_id":tt_data.tt_id,"tt_dept":tt_data.tt_dept,"tt_name":tt_data.tt_name,"tt_unique_id":tt_data.tt_unique_id,"tt_status":tt_data.tt_status,"tt_date":tt_data.tt_date,"tt_time":tt_data.tt_time})

def get_particular_tt(tt_id):
    tt_data = TimetableHistory.query.filter_by(tt_id = tt_id).first()
    mongoObjectId = str(tt_data.tt_unique_id)
    document = collection.find_one({'_id': ObjectId(mongoObjectId)})
    return json.dumps(document, default=json_util.default)

def delete_particular_tt(tt_id):
    tt_sql_id = TimetableHistory.query.get(tt_id)
    tt_data = TimetableHistory.query.filter_by(tt_id = tt_id).first()
    mongoObjectId = str(tt_data.tt_unique_id)
    if tt_sql_id:
        collection.delete_one({'_id': ObjectId(mongoObjectId)})
        db.session.delete(tt_sql_id)
        db.session.commit()
        return jsonify({"message":"TT Deleted Sucessfully"})

    return jsonify({"message":"Error 404"}),404


def updatett(tt_id):
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()
    tt_data = TimetableHistory.query.filter_by(tt_id = tt_id).first()

    ## Status Codes ##
    # NS = Not Sent
    # AP = Apporval Pending
    # TTC = Timetable Confirmed
    # TMP = Timetable Made Public
 
    if user.group == "ttfaculty":
        tt_data.tt_status = "AP"
        db.session.commit()
        return jsonify({"message": "Timetable sent for approval. Approval Pending"})
    elif user.group == "hod":
        tt_data.tt_status = "TTC"
        db.session.commit()
        return jsonify({"message": "Timetable is confirmed. Status Updated"})
    else:
        return jsonify("Message", "Unauthorized Error"), 401
    

def validate_publicity():
    count = TimetableHistory.query.filter_by(tt_is_public = "1").count()

    if count == 0:
        return True
    else:
        return False
    

# Only Admin function ####################
    
def makebacktonormal(tt_id):
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()
    if user.group == "superadmin":
        tt_data = TimetableHistory.query.filter_by(tt_id = tt_id).first()
        tt_data.tt_is_public = 0
        tt_data.tt_public_key = generate_password_hash(str(os.getenv('TT_PUBLIC_KEY')))
        db.session.commit()
        return jsonify({"Message":"Data Reseted"})
# Only Admin function ####################
    

def check_public(tt_id):
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()
    tt_data = TimetableHistory.query.filter_by(tt_id = tt_id).first()
    if validate_publicity():
        if tt_data.tt_is_public == "0" and check_password_hash(tt_data.tt_public_key,os.getenv('TT_PUBLIC_KEY')) and user.group == "ttfaculty":
            new_hash_status = generate_password_hash(str(os.getenv('FINAL_PUBLIC_KEY')))
            tt_data.tt_status = "TMP"
            tt_data.tt_public_key = new_hash_status
            tt_data.tt_is_public = "1"
            db.session.commit()
            return jsonify({"Message":"Made Public"})
        else:
            return jsonify({"message":"One is already public"})
    else:
        return jsonify({"message":"Process can't be done. One Timetable is already public"})


def get_public_data():
    tt_data = TimetableHistory.query.filter_by(tt_is_public = "1").first()

    if check_password_hash(tt_data.tt_public_key,os.getenv('FINAL_PUBLIC_KEY')):
        mongoObjectId = str(tt_data.tt_unique_id)
        document = collection.find_one({'_id': ObjectId(mongoObjectId)})
        return json.dumps(document, default=json_util.default)
    else:
        return jsonify({"message":"Error"})
    

def enrollment():
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()
    student_id = user.university_id
    section = request.json.get('section')
    course_number = request.json.get('course_number')
    course_name = request.json.get('course_name')
    room = request.json.get('room')
    instructor_id = request.json.get('instructor_id')
    instructor_name = request.json.get('instructor_name')
    pid = request.json.get('pid')
    time = request.json.get('time')
    day = request.json.get('day')
    enrollment_data = Enroll.query.filter_by(pid=pid,student_id=student_id)
    room_data = Timetable_course.query.all()
    for m in room_data:
        if m.max_numb_students != Enroll.query.filter_by(course_number=course_number).count():     
            for i in enrollment_data:
                if pid == i.pid and student_id == i.student_id:
                    return jsonify({"message":"You have already enrolled for this timeslot"})
                
                
    enrl = Enroll(student_id=student_id,section=section,course_number=course_number,course_name=course_name,room=room,instructor_id=instructor_id,instructor_name=instructor_name,pid=pid,time=time,day=day)
    db.session.add(enrl)
    db.session.commit()
    return {"message":"Enrollment successfully"}
            
            


def get_enrollment():
    data = []
    user_id = session.get("user_id")
    user = Authentication.query.filter_by(user_id=user_id).first()
    studid = user.university_id
    s_tt_data = Enroll.query.filter_by(student_id=studid)
    for dt in s_tt_data:
        data.append(
            {
                "student_id": dt.student_id,
                "section": dt.section,
                "course": {
                    "course_number": dt.course_number,
                    "course_name": dt.course_name
                },
                "room": dt.room,
                "instructor": {
                    "instructor_id": dt.instructor_id,
                    "instructor_name": dt.instructor_name
                },
                "meeting_time": {
                    "pid": dt.pid,
                    "time": dt.time,
                    "day": dt.day
                }
                }
        )
    return jsonify(data)


# Timetable Data
def rooms():
    data = Timetable_room.query.all()
    a=[]
    for i in data:
        a.append({"Id":i.id,
                  "r_number":i.r_number,
                  "seating_capacity": i.seating_capacity})   
        
    return a


def meetingtimes():
    data = Timetable_meetingtime.query.all()
    a=[]
    for i in data:
        a.append({"pid":i.pid,
                  "time":i.time,
                  "day": i.day})   
        
    return a

def instructors():
    data = Timetable_instructor.query.all()
    a=[]
    for i in data:
        a.append({"pid":i.id,
                  "time":i.uid,
                  "day": i.name})   
        
    return a

def departments():
    departments = Timetable_department.query.all()
    a=[]
    for i in departments:
        a.append(i.dept_name)   
        
    result = list(set(a))
    output= []
    for i,v in enumerate(result):
        output.append({
            "id":i+1,
            "dept_name": v
        })
    return output


def courses():
    data = Timetable_course.query.all()
    a=[]
    for i in data:
        a.append({"Id":i.course_number,
                  "r_number":i.course_name,
                  "seating_capacity": i.max_numb_students})   
        
    return a

def sections():
    data = Timetable_section.query.all()
    a=[]
    for i in data:
        dept_courses = Timetable_department_courses.query.filter_by(department_id=i.department_id).all()
        for m in dept_courses:
            course = Timetable_course.query.filter_by(course_number=str(m.course_id)).all()
            for j in course:
                a.append({
                    "Id": i.section_id,
                    "num_class_in_week": i.num_class_in_week,
                    "department_id": j.course_name
                })
        
    return a
    

# Testing 
def testview():
    data = Timetable_course.query.filter_by(course_number="BE01").all()
    a=[]
    for i in data:
        a.append({"Id":i.course_number,
                  "r_number":i.course_name,
                  "seating_capacity": i.max_numb_students})   
        
    return jsonify({"done":a})