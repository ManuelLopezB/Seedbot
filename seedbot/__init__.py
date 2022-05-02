from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from gpiozero import LED, Servo
from time import sleep
import os
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = '103b4cf3f6db7583cf1cd99537436c5d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from seedbot import routes
# led = LED(21)
# servo = Servo(17)
