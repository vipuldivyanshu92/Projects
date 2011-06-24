#!/usr/bin/env python

from twisted.internet.protocol import ReconnectingClientFactory
from RealmProtocol import RealmProtocol

class RealmClientFactory(ReconnectingClientFactory):
    protocol = RealmProtocol
    
    def startedConnecting(self, connector):
        print "Started to connect"
        
    def buildProtocol(self, addr):
        print "Connected"
        self.resetDelay()
        return self.protocol()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
    
    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)