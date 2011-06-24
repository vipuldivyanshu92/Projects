#!/usr/bin/env python

from twisted.internet.protocol import Protocol, ReconnectingClientFactory

class Connector(Protocol):    
    def connectionMade(self):
        self.transport.write("hello, world!")
    
    def dataReceived(self, data):
        print "Server said:", data
    
    def connectionLost(self, reason):
        print "connection lost"


class ConnectorFactory(ReconnectingClientFactory):
    protocol = Connector
    
    def startedConnecting(self, connector):
        print "Started to connect"
        
    def buildProtocol(self, addr):
        print "Connected"
        self.resetDelay()
        return ConnectorFactory.protocol()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
    
    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)