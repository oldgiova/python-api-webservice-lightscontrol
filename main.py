from flask import Flask, url_for, render_template, request, flash, redirect, session, abort
import RPi.GPIO as GPIO
import subprocess, os, logging 

import ipdb

'''initial VAR'''
RELAIS_4_GPIO = 2

logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
    )
app = Flask(__name__)

'''functions'''

# lights on
@app.route('/accendilucicortile', methods=['GET'])
def lights_on():
    logging.debug('accendi luci cortile')
    GPIO.output(RELAIS_4_GPIO, GPIO.LOW)
    logging.debug('Lights are on')
    return "<h1>Lights on</h1>"

# lights off
@app.route('/spegnilucicortile', methods=['GET'])
def lights_off():
    logging.debug('spegni luci cortile')
    GPIO.output(RELAIS_4_GPIO, GPIO.HIGH)
    logging.debug('Lights are off')
    return "<h1>Lights off</h1>"


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
