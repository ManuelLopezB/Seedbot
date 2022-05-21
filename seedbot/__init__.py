from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = '103b4cf3f6db7583cf1cd99537436c5d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from seedbot import routes
