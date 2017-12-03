#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
import RPi.GPIO as GPIO
import fileinput
from os import system
import signal
import sys

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

transmitter_pin = 17
receiver_pin = 27

GPIO.setup(transmitter_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(transmitter_pin, GPIO.IN)

outlets = [
    {
        "on": 11750924,
        "pulse": 169,
        "off": 11750916,
        "number": 1,
        "name": "Living room"
    },
    {
        "on": 11750922,
        "pulse": 169,
        "off": 11750914,
        "number": 2,
        "name": "Kitchen"
    },
    {
        "on": 11750921,
        "pulse": 169,
        "off": 11750913,
        "number": 3,
        "name": "Other Place"
    },
    {
        "on": 11750925,
        "pulse": 169,
        "off": 11750917,
    },
    {
        "on": 11750923,
        "pulse": 169,
        "off": 11750915,
    },
]

possible_actions = ["off", "on"]

# How many times will we send the RF signal?
max_tries = 3


def pre_shutdown(signum, frame):
    app.logger.warning("Cleaning up GPIO Pins")
    GPIO.cleanup()
    sys.exit(0)



signal.signal(signal.SIGINT, pre_shutdown)
signal.signal(signal.SIGTERM, pre_shutdown)


def send_rf_signal(code, pulse_length):
    system("/var/www/rfoutlet/codesend %(code)s -l %(pulse_length)s" % {
        "code": code,
        "pulse_length": pulse_length
    })


@app.route('/')
def hello_world():
    return 'Flask Dockerized; not much to see here'


@app.route('/outlets', methods=['GET'])
def outlet_list():
    return jsonify({'outlets': outlets})


@app.route('/outlets/<int:outlet_number>', methods=['GET'])
def outlet_detail(outlet_number):
    return jsonify({'outlet': outlets[outlet_number-1]})


@app.route('/outlets/<int:outlet_number>/<string:outlet_action>', methods=['POST'])
def outlet_action(outlet_number, outlet_action):
    app.logger.info("I'm being told to perform '%(action)s' for outlet '%(number)s'" % {
        "action": outlet_action,
        "number": outlet_number
    })
    if (outlet_action not in possible_actions):
        return jsonify({"error": "Unsupported action: " + outlet_action})

    # Actually send the RF signal to turn the outlet on or off; sometimes it takes a few times
    for i in range(0, max_tries):
        send_rf_signal(outlets[outlet_number-1][outlet_action], outlets[outlet_number-1]['pulse'])

    return jsonify({"outlet": outlets[outlet_number-1]})


if __name__ == '__main__':
    handler = RotatingFileHandler('/var/log/light_control_server/flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
    app.logger.warning("About to start the server...")
