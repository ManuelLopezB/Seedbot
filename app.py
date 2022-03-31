from time import sleep

from flask import Flask, render_template, url_for

from gpiozero import LED

app = Flask(__name__)
led = LED(21)


@app.route("/")
@app.route("/home")
def home():
    led.off()
    return render_template('home.html', tittle='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/on')
def on():
   led.on()
   return 'Led On'

@app.route('/off')
def off():
   led.off()
   return 'Led Off'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
