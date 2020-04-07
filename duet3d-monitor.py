#!./env/bin/python

import os, sys, time, logging, json, random, requests
import google
import googlesay
import configparser

logging.basicConfig(format='%(asctime)s: %(levelname)s %(message)s', filename="runtime.log", level=logging.WARN)
logger = logging.getLogger()
logger.info('Logging started')

config = configparser.ConfigParser()
config.read('config.ini')


def check() -> str:
    logger.info('Checking printer status...')

    logger.debug('Trying to get status url from config...')
    url = config.get('API', 'status_url')
    logger.debug('url: %s' % url)

    response = requests.get(url)
    logger.debug('request performed!')

    logger.debug('API response: %s' % response)
    data = response.json()

    return data.get(config.get('API', 'status_json_property_name')) 


def tell(message: str):
    if message in googlesay.messages:
        logger.info('Trying to tell "%s"' % message)
        googlesay.say(message)


def tick(self = None):
    status_filename = '/tmp/duet3d_last_status.txt'

    previous_status = ''
    with open(status_filename, 'r') as previous:
        previous_status = previous.readline()

    current_status = check()

    if current_status != previous_status:
        logger.info('Status changed from %s to %s' % (previous_status, current_status))
        
        with open(status_filename, 'w+') as previous:
            previous.write(current_status)
        
        tell(current_status)

    time.sleep(float(config.get('API', 'delay_seconds').replace(',','.'))) 


if __name__ == "__main__":
    print("Running")
    while True:
        tick()
