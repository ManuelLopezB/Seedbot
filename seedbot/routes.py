from flask import Response, render_template, flash, redirect, url_for, Flask, jsonify
from seedbot import app
from seedbot.models import User
from seedbot.forms import LoginForm
import serial
import time
import cv2
import os

try:
    arduino = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
except:
    try:
        arduino = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
    except:
        pass


if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    video = cv2.VideoCapture(0)


@app.route('/')
@app.route('/home')
def home():
    try:
        time.sleep(1)
        arduino.flushInput()
        arduino.setDTR(True)
        time.sleep(2)
    except:
        pass
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
    ack = arduino.readline().strip()
    return render_template('about.html', title='About', segment='about', ack=ack)


@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin', segment='admin')


@app.route('/humedad')
def humedad():
    ack = arduino.read()
    return jsonify(number = ack)

@app.route('/siembra_t')
def siembra_t():
    arduino.write(b'3')
    return ("nothing")

@app.route('/preparar_t')
def preparar_t():
    arduino.write(b'2')
    return ("nothing")


@app.route('/riego_t')
def riego_t():
    arduino.write(b'1')
    return ("nothing")


@app.route('/apagar')
def apagar():
    arduino.write(b'0')
    return ("nothing")


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
