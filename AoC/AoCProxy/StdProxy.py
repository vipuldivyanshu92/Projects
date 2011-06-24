"""
Faolan Project, a free Age of Conan server emulator made for educational purpose
Copyright (C) 2008 Project Faolan team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

#!/usr/bin/env python

import asyncore
import socket
import struct

# The main class of the Proxy
class proxy_server (asyncore.dispatcher):    
    def __init__ (self, host, port, bindport):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP Socket
        self.set_reuse_addr()       # Set this socket as reusable
        self.there = (host, port)   # Remote server connection
        self.bind(('', bindport))   # Bind a server localy on bindport
        self.listen(5)              # Listen for 5 incomming connection

    def handle_accept(self):
        proxy_receiver(self, self.accept())     # Create a proxy_receiver object, with a socket object as parameter
        
# Establish the connection between the proxy and the server
class proxy_sender (asyncore.dispatcher):
    def __init__ (self, receiver, address):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver                                # Get the receiver object
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP Socket
        self.connect(address)                                   # Connect to the server
        
        # Create buffers for incoming and outgoing datas
        self.read_buffer = []       # Buffer for incoming packets, before they are parsed
        self.write_buffer = []      # buffer for outgoing packets each element is a packet

    def handle_connect (self):
        pass
        
    def handle_expt(self):
        self.close()                # connection failed, shutdown
    
    def handle_read(self):
        buffer = self.recv(4096)             # Read a buffer of 4k append to the read_buffer string            
        self.receiver.write_buffer += [buffer]    # Add this packet into the write buffer of the receiver 
        print "%s:%d -> %s:%d  %d bytes" % (self.receiver.server.there[0], self.receiver.server.there[1], self.receiver.addr[0], self.receiver.addr[1], len(buffer))
        print buffer.encode("hex")
        print
            
    def handle_write(self):
        self.send(self.write_buffer[0])
        del self.write_buffer[0]
    
    def writable(self):                     # Called if the socket is writable
        return len(self.write_buffer) > 0

    def handle_close (self):
         self.receiver.close()
         self.close()

# Establish the connection between the client and the proxy
class proxy_receiver (asyncore.dispatcher):
    def __init__ (self, server, (conn, addr)):
        asyncore.dispatcher.__init__(self, conn)
        self.server = server
        self.sender = proxy_sender(self, server.there)
        self.addr = addr
        
        # Create buffers for incoming and outgoing datas
        self.read_buffer = ''
        self.write_buffer = []
        
    def handle_connect (self):
        print 'Connected'
        
    def handle_expt(self):
        self.close() # connection failed, shutdown
    
    def handle_read(self):
        buffer = self.recv(4096)
        self.sender.write_buffer += [buffer]
        print "%s:%d -> %s:%d  %d bytes" % (self.addr[0], self.addr[1], self.server.there[0], self.server.there[1], len(buffer))
        print buffer.encode("hex")
        print
    
    def handle_write(self):
        self.send(self.write_buffer[0])
        del self.write_buffer[0]
    
    def writable(self):                     # Called if the socket is writable
        return len(self.write_buffer) > 0   # Allow to write only if something can be written

    def handle_close (self):
         print 'Closing'
         self.sender.close()
         self.close()
