#!/usr/bin/env python

# Import required librairies
import asyncore
import socket
import struct
from libs import *

class UniverseHandler(asyncore.dispatcher):    
    def __init__(self):                                         # Parameters for the connection
        asyncore.dispatcher.__init__(self)                      # Overload the previous definition
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the sock_stream socket
        self.connect(('127.0.0.1', 7000))                       # Connect to the realm_server
        self.buffer = []

        self.packethandler = {                                  # Dictionnary with received opcode and function to call
            0x0000 : self.Challenge,
        }
        
        self.onsent = {
            #0x0000 : self.
        }

    def InitiateAuthentication(self):
        pkt = packet('UniverseAgent', 'UniverseInterface', 0x00)
        pkt.append('H', 0x0000)
        pkt.appendpwstr('Adraen:2')
        pkt.append('I', 0x00000001)
        
        self.buffer += [pkt]
        
    def Challenge(self, pkt):
        serverHash = pkt.data[2:]
        print serverHash
        
    def Unknown(self, pkt):
        print "Unknown packet %s" % hex((pkt.opcode))
        print

    def handle_connect(self):
        print "Connection successfull"
        print
        self.InitiateAuthentication()

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        pkt = packet('UniverseAgent', 'UniverseInterface')
        pkt.set(self.recv(4096))
        print "%d bytes read" % (pkt.size())
        self.packethandler.get(pkt.opcode, self.Unknown)(pkt)

    def handle_write(self):
        if self.buffer:
            sent = self.send(self.buffer[0].get())
            print "%d bytes written" % (sent)
            #print self.buffer[0].encode('hex')
            print
            
            if self.onsent.has_key(self.buffer[0].opcode):
                self.onsent[self.buffer[0].opcode](self.buffer[0])
                
            del self.buffer[0]

    def handle_close(self):
        print "Connection closed."
        self.close()
        
userv = UniverseHandler()
asyncore.loop()

raw_input()