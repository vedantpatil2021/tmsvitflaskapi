from application import app
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'tmsvit'

app.config["MONGO_URI"] = "mongodb://localhost:27017/tmsvit"
mongo = PyMongo(app).db
mysql = MySQL(app)
