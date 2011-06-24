#!/usr/bin/env python

from twisted.internet import reactor
from realm.RealmClientFactory import RealmClientFactory

f = RealmClientFactory()
reactor.connectTCP("wow.avalonserver.org", 3724, f)
reactor.run()