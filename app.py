from flask import Flask, Response, render_template
from gpiozero import LED
import cv2

app = Flask(__name__)
# led = LED(21)
video = cv2.VideoCapture(0)


@app.route("/")
@app.route("/home")
def home():
    # led.off()
    return render_template('home.html', tittle='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/on')
def on():
#    led.on()
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
    app.run(host='0.0.0.0', threaded=True)