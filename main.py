import RPi.GPIO as GPIO
import fileinput
from os import system

GPIO.setmode(GPIO.BCM)

transmitter_pin = 17
receiver_pin = 27

GPIO.setup(transmitter_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(transmitter_pin, GPIO.IN)

outlets = [
    {
        "on": 11750924,
        "pulse": 169,
        "off": 11750916
    },
    {
        "on": 11750922,
        "pulse": 169,
        "off": 11750914
    },
    {
        "on": 11750921,
        "pulse": 169,
        "off": 11750913
    },
    {
        "on": 11750925,
        "pulse": 169,
        "off": 11750917
    },
    {
        "on": 11750923,
        "pulse": 169,
        "off": 11750915
    },
]

def send_rf_signal(code, pulse_length):
    system("/var/www/rfoutlet/codesend %(code)s -l %(pulse_length)s" % {
        "code": code,
        "pulse_length": pulse_length
    })

while True:
    light_number = None
    action = None
    while (light_number is None or light_number > len(outlets) or light_number < 0):
        try:
            light_number = int(raw_input("Please enter the light number you wish to control: ")) - 1
        except ValueError:
            pass

    print("Great!")
    while (action != 'on' and action != 'off'):
        action = raw_input("Now type 'on' or 'off' for the action you wish to perform: ")
    
    send_rf_signal(outlets[light_number][action], outlets[light_number]['pulse'])
