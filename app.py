from email.policy import default
from flask import Flask, Response, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
# from gpiozero import LED, Servo
from time import sleep
from datetime import datetime
import os
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = '103b4cf3f6db7583cf1cd99537436c5d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# led = LED(21)
# servo = Servo(17)
if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    video = cv2.VideoCapture(0)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.date_added}')"




@app.route('/')
@app.route('/home')
def home():
    # led.off()
    return render_template('home.html', title='Home', segment='home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form, segment='login')

@app.route('/about')
def about():
    return render_template('about.html', title='About', segment='about')

@app.route('/on')
def on():
    return render_template('home.html', title='Led On')

@app.route('/off')
def off():
#    led.off()
   return render_template('home.html', title='Led Off')

@app.route('/admin')
def admin():
#    led.off()
   return render_template('admin.html', title='Admin', segment='admin')

def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)