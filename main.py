from flask import Flask, url_for, render_template, request, flash, redirect, session, abort, jsonify
import RPi.GPIO as GPIO
import subprocess, os, logging 
import ipdb
from config import Config
from time import sleep

'''initial VAR'''
# Light GPIO
RELAIS_4_GPIO = 2
# Water GPIO
RELAIS_WATER_GPIO = 22

logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
    )
app = Flask(__name__)
app.config.from_object(Config)
TOKEN = app.config['TOKEN']

'''functions'''

# Turn the light on
@app.route('/accendilucicortile', methods=['POST'])
def lights_on():
    token = request.json.get('token', None)
    if token != TOKEN:
        logging.debug('not authorized access')
        return jsonify({"msg": "Unauthorized"}), 400
    elif token == TOKEN:
        logging.debug('Turn the lights on')
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
        logging.debug('Turn the lights off')
        GPIO.output(RELAIS_4_GPIO, GPIO.HIGH)
        logging.debug('Lights are off')
        return jsonify({"msg": "Lights off"}), 200
    else:
        return jsonify({"msg": "This should never happen"}), 200

# water on
@app.route('/accendiacqua', methods=['POST'])
def water_on():
    token = request.json.get('token', None)
    if token != TOKEN:
        logging.debug('not authorized access')
        return jsonify({"msg": "Unauthorized"}), 400
    elif token == TOKEN:
        GPIO.output(RELAIS_WATER_GPIO, GPIO.LOW)
        logging.debug('Starting irrigation')
        sleep(5)
        if GPIO.input(RELAIS_WATER_GPIO):
            logging.error('Irrigation not started')
        else:
            logging.debug('Irrigation correctly started')
        return "<h1>Irrigation is on</h1>"
    else:
        return jsonify({"msg": "This should never happen"}), 200

# water off
@app.route('/spegniacqua', methods=['POST'])
def water_off():
    token = request.json.get('token', None)
    if token != TOKEN:
        logging.debug('not authorized access')
        return jsonify({"msg": "Unauthorized"}), 400
    elif token == TOKEN:
        GPIO.output(RELAIS_WATER_GPIO, GPIO.HIGH)
        logging.debug('Stopping Irrigation')
        sleep(5)
        if GPIO.input(RELAIS_WATER_GPIO):
            logging.debug('Irrigation correctly stopped')
        else:
            logging.error('Irrigation not stopped')
        return "<h1>Irrigation is off</h1>"
    else:
        return jsonify({"msg": "This should never happen"}), 200


if __name__ == '__main__':
    logging.info('starting up')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAIS_4_GPIO,GPIO.OUT, initial=GPIO.HIGH) #lights off
    if GPIO.input(RELAIS_4_GPIO):
        logging.debug('Luce spenta')
    else:
        logging.debug('Luce accesa')
    GPIO.setup(RELAIS_WATER_GPIO, GPIO.OUT, initial=GPIO.HIGH) #water off
    if GPIO.input(RELAIS_WATER_GPIO):
        logging.debug('Irrigazione spenta')
    else:
        logging.debug('Irrigazione accesa')
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
        GPIO.output(RELAIS_WATER_GPIO, GPIO.HIGH)
        GPIO.cleanup()
