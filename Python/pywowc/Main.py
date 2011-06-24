#!/usr/bin/env python

import asyncore
from shared import Connector
from realm import RealmHandler, RealmProtocol
import ConfigParser

# Retrieve the configuration
config = ConfigParser.RawConfigParser()
config.read('config.conf')

# Get realm host and port from the config
realmhost = config.get('realm', 'host')
realmport = config.getint('realm', 'port')

# create a protocol and a handler for the realm
realmProtocol = RealmProtocol.RealmProtocol()
realmHandler = RealmHandler.RealmHandler()

# connect to the remote server
realmconnector = Connector.Connector(realmhost, realmport, realmProtocol, realmHandler)

# (todo) add filters
"""
realmconnector.addOnRecvFilter()
realmconnector.addOnSendFilter()
realmconnector.addOnHandle()

realmhandler.addOnPacket()
"""


asyncore.loop()