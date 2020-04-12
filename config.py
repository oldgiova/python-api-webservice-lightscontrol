import os

class Config(object):
    TOKEN = os.environ.get('TOKEN') or 'you-will-never-guess'
