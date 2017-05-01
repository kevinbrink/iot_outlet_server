import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
app = Flask(__name__)


lights = [
    {
        "number": 1,
        "name": "Living room"
    },
    {
        "number": 2,
        "name": "Kitchen"
    },
    {
        "number": 3,
        "name": "Basement"
    },
]

possible_actions = ["off", "on"]


@app.route('/')
def hello_world():
    return 'Flask Dockerized; not much to see here'


@app.route('/lights', methods=['GET'])
def light_list():
    return jsonify({'lights': lights})


@app.route('/lights/<int:light_number>', methods=['GET'])
def light_detail(light_number):
    return jsonify({'light': lights[light_number-1]})


@app.route('/lights/<int:light_number>/<string:light_action>', methods=['POST'])
def light_action(light_number, light_action):
    app.logger.info("I'm being told to perform '%(action)s' for light '%(number)s'" % {
        "action": light_action,
        "number": light_number
    })
    if (light_action not in possible_actions):
        return jsonify({"error": "Unsupported action: " + light_action})

    # TODO: Here, you would actually perform the light turning on / off

    return jsonify({"light": lights[light_number-1]})


if __name__ == '__main__':
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
