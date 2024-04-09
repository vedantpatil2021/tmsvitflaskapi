from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash

from application import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/tmsvit'
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'

app.app_context().push()

db = SQLAlchemy(app)

class Authentication(db.Model):
    user_id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    username = db.Column(db.String(25),unique=True,nullable=False)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(60),nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
    password_hash = db.Column(db.String(100))
    group = db.Column(db.String(55),nullable=False)
    is_super_user = db.Column(db.String(5))
    last_login = db.Column(db.String(50),nullable=False)
    date_joined = db.Column(db.String(50),nullable=False)
    dept = db.Column(db.String(10),nullable=False)
    university_id = db.Column(db.String(10),nullable=False)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)



class TimetableHistory(db.Model):
    tt_id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    tt_dept = db.Column(db.String(5),nullable=False)
    tt_name = db.Column(db.String(100),nullable=False)
    tt_unique_id = db.Column(db.String(100),nullable=False)
    tt_status = db.Column(db.String(200),nullable=False)
    tt_date = db.Column(db.String(200),nullable=False)
    tt_time = db.Column(db.String(200),nullable=False)
    tt_is_public = db.Column(db.String(200),nullable=False)
    tt_public_key = db.Column(db.String(100),nullable=False)


class Enroll(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    student_id = db.Column(db.String(200),nullable=False)
    section = db.Column(db.String(200),nullable=False)
    course_number = db.Column(db.String(200),nullable=False)
    course_name = db.Column(db.String(200),nullable=False)
    room = db.Column(db.String(200),nullable=False)
    instructor_id = db.Column(db.String(200),nullable=False)
    instructor_name = db.Column(db.String(200),nullable=False)
    pid = db.Column(db.String(200),nullable=False)
    time = db.Column(db.String(200),nullable=False)
    day = db.Column(db.String(200),nullable=False)
    
class Timetable_room(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    r_number = db.Column(db.String(6),nullable=False)
    seating_capacity = db.Column(db.Integer,autoincrement = True)
    
    
class Timetable_meetingtime(db.Model):
    pid = db.Column(db.Integer,primary_key=True,autoincrement = True)
    time = db.Column(db.String(50),nullable=False)
    day = db.Column(db.String(15),nullable=False)
    
class Timetable_instructor(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    uid = db.Column(db.String(6),nullable=False)
    name = db.Column(db.String(25),nullable=False)
    
class Timetable_department(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    dept_name = db.Column(db.String(50),nullable=False)
    
class Timetable_department_courses(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement = True)
    department_id = db.Column(db.Integer,autoincrement = True)
    course_id = db.Column(db.String(5),nullable=False)
    
class Timetable_course(db.Model):
    course_number = db.Column(db.String(5),primary_key=True,autoincrement = True)
    course_name = db.Column(db.String(40),nullable=False)
    max_numb_students = db.Column(db.String(65),nullable=False)
    
class Timetable_section(db.Model):
    section_id = db.Column(db.String(25),primary_key=True)
    num_class_in_week = db.Column(db.Integer,nullable=False)
    course_id = db.Column(db.String(5))
    department_id = db.Column(db.Integer)
    instructor_id = db.Column(db.Integer)
    meeting_time_id = db.Column(db.String(4))
    room_id = db.Column(db.Integer)