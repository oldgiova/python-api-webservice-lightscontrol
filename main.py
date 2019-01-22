from flask import Flask, url_for, render_template, request, flash, redirect, session, abort, jsonify
import RPi.GPIO as GPIO
import subprocess, os, logging 
import ipdb

'''initial VAR'''
RELAIS_4_GPIO = 2
TOKEN = 'aserwrkljlkdgsdglkj12e230'

logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
    )
app = Flask(__name__)

'''functions'''

# lights on
@app.route('/accendilucicortile', methods=['POST'])
def lights_on():
    token = request.json.get('token', None)
    if token != TOKEN:
        logging.debug('not authorized access')
        return jsonify({"msg": "Unauthorized"}), 400
    elif token == TOKEN:
        logging.debug('accendi luci cortile')
        GPIO.output(RELAIS_4_GPIO, GPIO.LOW)
        logging.debug('Lights are on')
        return jsonify({"msg": "Lights on"}), 200
    else:
        return jsonify({"msg": "This should never happen"}), 200

# lights off
@app.route('/spegnilucicortile', methods=['POST'])
def lights_off():
    token = request.json.get('token', None)
    if token != TOKEN:
        logging.debug('not authorized access')
        return jsonify({"msg": "Unauthorized"}), 400
    elif token == TOKEN:
        logging.debug('spegni luci cortile')
        GPIO.output(RELAIS_4_GPIO, GPIO.HIGH)
        logging.debug('Lights are off')
        return jsonify({"msg": "Lights off"}), 200
    else:
        return jsonify({"msg": "This should never happen"}), 200


if __name__ == '__main__':
    logging.info('starting up')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAIS_4_GPIO,GPIO.OUT, initial=GPIO.HIGH)
    app.secret_key = os.urandom(12)
    try:
        app.run(
                debug=True,
                host='0.0.0.0',
                port=5000
                )
    except:
        logging.info('exception')
    finally:
        GPIO.cleanup()
