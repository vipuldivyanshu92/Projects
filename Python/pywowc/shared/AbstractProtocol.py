#!/usr/bin/env python

class AbstractProtocol:
    """
        Interface for protocol design
    """
    
    def getPacketFromStream(self, s):
        """
            Should return a None object with a readed length of 0
            if no packet is aivalable, and a packet object of length
            of data read.
        """
        pass
