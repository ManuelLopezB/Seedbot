from flask import Flask, Response, render_template, flash, redirect, url_for
from forms import LoginForm
from gpiozero import LED, Servo
from time import sleep
import os
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = '103b4cf3f6db7583cf1cd99537436c5d'
# led = LED(21)
servo = Servo(17)
if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    video = cv2.VideoCapture(0)

@app.route('/')
@app.route('/home')
def home():
    # led.off()
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/on')
def on():
#    led.on()
    servo.mid()
    print("mid")
    sleep(0.5)
    servo.min()
    print("min")
    sleep(1)
    servo.mid()
    print("mid")
    sleep(0.5)
    servo.max()
    print("max")
    sleep(1)
    return render_template('home.html', title='Led On')

@app.route('/off')
def off():
#    led.off()
   return render_template('home.html', title='Led Off')

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