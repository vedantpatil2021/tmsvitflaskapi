from flask import Flask
from flask_cors import CORS
from flask_session import Session
from config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
Session(app)
CORS(app,supports_credentials=True)

