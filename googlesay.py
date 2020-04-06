#
# spoke something on GoogleHome
#
# use: ./ghome_say [ghome_ip] [text_to_say]
#
#

import sys
import pychromecast
import os
import os.path
from gtts import gTTS
import time
import hashlib
import logging
import configparser

messages = ('P', 'I')

def say(message: str):
   logger = logging.getLogger()
   config = configparser.ConfigParser()
   config.read('config.ini')

   if message not in messages:
      logger.warning('Tried to play message that is not defined: %s' % messages)

   url_format = config.get('AUDIO', 'url_format')
   logger.debug('Audio message URL format: %s' % url_format)

   url = url_format % str.lower(message)
   logger.info('Trying to play %s' % url)

   device_ip = config.get('CHROMECAST', 'ip_address')

   castdevice = pychromecast.Chromecast(device_ip)
   castdevice.wait()

   mc = castdevice.media_controller
   mc.play_media(url, "audio/mp3")

   mc.block_until_active()

   mc.pause() #prepare audio and pause...

   time.sleep(1.2)

   mc.play() #play the mp3

   while not mc.status.player_is_idle:
      time.sleep(0.5)

   mc.stop()

   castdevice.quit_app()