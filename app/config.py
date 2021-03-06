import os
import configparser
from itertools import chain

BRAND_NAME = 'Falcon REST API Template'

APP_ENV = os.environ.get('APP_ENV') or 'dev'
INI_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../conf/{}.ini'.format(APP_ENV))

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)
POSTGRES = CONFIG['postgres']
if APP_ENV == 'dev' or APP_ENV == 'live':
    DB_CONFIG = (POSTGRES['user'], POSTGRES['password'], POSTGRES['host'], POSTGRES['database'])    
    DATABASE_URL = "postgres://%s:%s@%s:5432/%s" % DB_CONFIG
else:
    DB_CONFIG = (POSTGRES['user'], POSTGRES['password'], POSTGRES['host'], POSTGRES['database'])    
    DATABASE_URL = "postgres://%s:%s@%s:5432/%s" % DB_CONFIG

DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG['logging']['level']