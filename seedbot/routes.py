from flask import Response, render_template, flash, redirect, url_for, Flask
from seedbot import app
from seedbot.models import User
from seedbot.forms import LoginForm
import serial
import cv2
import os

arduino = serial.Serial('/dev/ttyACM0', 9600)

if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    video = cv2.VideoCapture(0)

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

@app.route('/riego_v')
def riego_v():
    arduino.write("rv")
    return render_template('home.html')

@app.route('/riego_f')
def riego_f():
    arduino.write("rf")
    return render_template('home.html')

@app.route('/admin')
def admin():
#    led.off()
   return render_template('admin.html', title='Admin', segment='admin')

def gen(video):
    while True:
        success, image = video.read()
        # Para girar la imagen ROTATE_90_CLOCKWISE ROTATE_180
        # image = cv2.rotate(image, cv2.cv2.ROTATE_180)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
