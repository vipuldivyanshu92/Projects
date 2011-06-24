import asyncore
import logging
from realmproxy import RealmServer
from worldproxy import WorldServer
from keyserver import KeyServer
from config import config

### Setup the logger
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

# set up logging to file
logging.basicConfig(level=LEVELS.get(config.get('LOGGER', 'filelevel'), logging.NOTSET),
                    format='%(asctime)s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename=config.get('LOGGER', 'filename'),
                    filemode='a')

# define a Handler which writes messages to the sys.stderr
console = logging.StreamHandler()
console.setLevel(LEVELS.get(config.get('LOGGER', 'consolelevel'), logging.NOTSET))

# set a format which is simpler for console use
formatter = logging.Formatter('%(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)


### Setup the proxy
env = dict()

env['key'] = None
env['realm'] = {'socket' : RealmServer(config.getint('REALM', 'localport'), config.get('REALM', 'remotehost'), config.getint('REALM', 'remoteport'), env)}
env['world'] = {'socket' : WorldServer(config.getint('WORLD', 'localport'), config.get('WORLD', 'remotehost'), config.getint('WORLD', 'remoteport'), env)}
env['keyserver'] = {'socket' : KeyServer(config.getint('KEYSERVER', 'localport'), env)}

asyncore.loop()
