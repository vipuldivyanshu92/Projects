#!/usr/bin/env python

class AbstractHandler:
    
    def connectionEstablished(self, session):
        pass
    
    def connectionClosed(self, session):
        pass
    
    def connectionException(self, session):
        pass
    
    def packetReceived(self, session, packet):
        pass
    
    def packetSent(self, session, packet):
        pass
    