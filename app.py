from flask import Flask
from gpiozero import LED
from signal import pause

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/blink")
def blink():
    led = LED(17)
    led.blink()
 