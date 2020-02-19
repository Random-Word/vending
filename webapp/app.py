from flask import Flask
import RPi.GPIO as GPIO
import time
import pymysql
import json

with open('../credentials.json', 'r') as credsfile:
    creds = json.load(credsfile)

db_connection = pymysql.connect(host=creds["host"], user=creds["user"], password=creds["password"], db=creds["db"], cursorclass=pymysql.cursors.DictCursor)
db_cursor = db_connection.cursor()

app = Flask(__name__)

"""
PIN number: Vending machine rail label
1: NOT CONNECTED
2: Y
3: X
4: U
5: W
6: O
7: N/C
8: N/C
9: HH
10: GG
11: R
12: N/C
13: P
14: N/C
15: N/C
16: N/C
17: V
19: M
20: Y
21: N/C
22: S
23: N/C
24: N/C
26: N
27: T
"""

pin_lookup = {
        1: "NOT CONNECTED",
        2: "Y",
        3: "X",
        4: "U",
        5: "W",
        6: "O",
        7: "N/C",
        8: "N/C",
        9: "HH",
        10: "GG",
        11: "R",
        12: "N/C",
        13: "P",
        14: "N/C",
        15: "N/C",
        16: "N/C",
        17: "V",
        19: "M",
        20: "Y",
        21: "N/C",
        22: "S",
        23: "N/C",
        24: "N/C",
        26: "N",
        27: "T",}

good_pins = [2, 3, 4, 5, 6, 9, 10, 11, 13, 17, 19, 20, 22, 26, 27]

rail_lookup = {pin_lookup[pin]: pin for pin in good_pins}

@app.route('/')
def hello_world():
    return "Hello, I'm a Vending Machine!"

def activate_pin(pin, duration=1):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(duration)
    GPIO.cleanup()

@app.route('/pin/<int:pin>')
def web_to_pin(pin):
    activate_pin(pin, 1.5)
    vending_rail = pin_lookup.get(pin) or "Not Connected"
    return "Activated pin {}, which maps to rail {}.".format(pin, vending_rail)

@app.route('/rail/<string:rail>')
def web_to_rail(rail):
    pin_to_use = rail_lookup.get(rail)
    if pin_to_use:
        activate_pin(pin_to_use, 1.5)
        return "Vending rail {}.".format(rail)
    else:
        return "Sorry, we can't vend from rail {}. Available rails are: {}.".format(rail, ", ".join([pin_lookup[pin] for pin in good_pins]))

@app.route('/product/add/<string:name>')
def add_product(name):
    query = "INSERT INTO Products (name, description, price) values ('{}', 'dummy description', 10.00);".format(name)
    db_cursor.execute(query)
    return "Added {}.".format(name)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
 
