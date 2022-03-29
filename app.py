from time import sleep

from flask import Flask
from gpiozero import LED

app = Flask(__name__)
led = LED(21)


@app.route("/")
def hello_world():
    led.close()
    return "Seedbot"

@app.route('/on')
def on():
   led.on()
   return 'Led Encendido'

@app.route('/off')
def off():
   led.off()
   return 'Led Apagado'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
