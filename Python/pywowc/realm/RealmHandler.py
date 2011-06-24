#!/usr/bin/env python

from .shared.AbstractHandler import AbstractHandler

class RealmHandler(AbstractHandler):
    def connectionEstablished(self, session):
        """ Implied by the first read or write event """
        session.write("momo")
    
    def connectionClosed(self, session):
        pass
    
    def connectionException(self, session):
        pass
    
    def packetReceived(self, session, packet):
        pass
    
    def packetSent(self, session, packet):
        pass
