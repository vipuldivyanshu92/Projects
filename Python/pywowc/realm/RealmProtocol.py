#!/usr/bin/env python

from .shared.AbstractProtocol import AbstractProtocol

class RealmProtocol(AbstractProtocol):
    
    def getPacketFromStream(self, s):
        if s:
            return s, len(s)
        else:
            return None, 0

