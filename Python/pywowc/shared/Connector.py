#!/usr/bin/env python

import asyncore
import socket

class Connector(asyncore.dispatcher):
    BUFFER_SIZE = 4096
    
    def __init__(self, host, port, protocol, handler):
        asyncore.dispatcher.__init__(self)
        
        # Create the reading and writing buffers
        self.writeBuffer = []
        self.readBuffer = ""
        
        # Define the protocol and handler
        self.handler = handler
        self.protocol = protocol
        
        # Connect to the realm server
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
    def write(self, pkt):
        self.writeBuffer.append(pkt)
        
    def handle_connect(self):
        self.handler.connectionEstablished(self)
        
    def handle_expt(self):
        self.handler.connectionException(self)
        self.close()
        
    def handle_read(self):
        self.readBuffer.join(self.recv(Connector.BUFFER_SIZE))
        
        # read every possible packets from the stream
        pkt, size = self.protocol.getPacketFromStream(self.readBuffer)
        while pkt:
            self.handler.packetReceived(self, packet)
            self.readBuffer = self.readBuffer[size:]
            pkt, size = self.protocol.getPacketFromStream(self.readBuffer)
        
    def writable(self):
        return (len(self.writeBuffer) > 0)
        
    def handle_write(self):
        pkt = self.writeBuffer.pop(0)
        self.send(pkt)
        self.handler.packetSent(self, pkt)
        
    def handle_close(self):
        self.handler.connectionClosed(self)
        self.close()
        