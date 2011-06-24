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
from shared.packet import *
from shared.realm import *
import StdProxy

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
        self.read_buffer = ''       # Buffer for incoming packets, before they are parsed
        self.write_buffer = []      # buffer for outgoing packets each element is a packet

    def handle_connect (self):
        pass
        
    def handle_expt(self):
        self.close()                # connection failed, shutdown
    
    def handle_read(self):
        self.read_buffer += self.recv(4096)             # Read a buffer of 4k append to the read_buffer string
        while self.read_buffer:                         # for each packet in the read_buffer
            pkt = packet()                              # Create a packet object
            pkt.ReadFromBuffer(self.read_buffer, False)
            
            if pkt.size > len(self.read_buffer):        # If the packet is not full we go out of the while loop
                break
            
            if pkt.sender == "UniverseAgent":
                if pkt.opCode == 1:
                    status = struct.unpack('!I', pkt.data[:4])[0]
                    # 0x00000001 mean right login informations
                    if status == 0x00000001:
                        unk2, unk3, realmLength = struct.unpack('!IIH', pkt.data[4:14])
                        realmAdress, unk4, unk5 = struct.unpack('!%dsII' % (realmLength), pkt.data[14:])
                        realmAdress = realmAdress.split(':')
                        print 
                        CharServer = proxy_server(realmAdress[0], int(realmAdress[1]), 7001)
                        realmAdress = '%s:7001' % (self.receiver.addr[0])
                        print self.receiver.addr[0]
                        realmLength = len(realmAdress)
                        pkt.data = struct.pack('!IIIH%dsII' % (realmLength), status, unk2, unk3, realmLength, realmAdress, unk4, unk5)
                                                                    
                    # 0xffffffff mean a failed login (wrong password)
                    elif status == 0xffffffff:
                        #unk1, unk2, unk3, unk4, unk5 = struct.unpack('!IIIIH', )
                        pkt.data = pkt.data[:20] + struct.pack('!H', 0x0000)
                    
            elif pkt.sender == "PlayerAgent":
                if pkt.opCode == 5:
                    rlmEnum = realmEnum()
                    rlmEnum.ReadFromBuffer(pkt.data)
                
            elif pkt.sender == "ServerInterface":
                if pkt.opCode == 2:
                    WorldAddr = struct.unpack('!BBBBH', pkt.data[:6])
                    Unk1Addr = struct.unpack('!BBBBH', pkt.data[6:12])
                    print WorldAddr
                    print Unk1Addr
                    pkt.data = struct.pack('!BBBBHBBBBH', 127, 0, 0, 1, 7040, 127, 0, 0, 1, 7038)+pkt.data[12:]
                    #WorldServer = proxy_server('%d.%d.%d.%d' % WorldAddr[:4], WorldAddr[4], 7040)
                    WorldServer = StdProxy.proxy_server('%d.%d.%d.%d' % WorldAddr[:4], WorldAddr[4], 7040)
                    Unk1Server  = StdProxy.proxy_server('%d.%d.%d.%d' % Unk1Addr[:4], Unk1Addr[4], 7038)
                    
                elif pkt.opCode == 3:
                    CSPlayerInterfaceAddr = struct.unpack('!BBBBH', pkt.data[:6])
                    print CSPlayerInterfaceAddr
                    pkt.data = struct.pack('!BBBBH', 127, 0, 0, 1, 7037)+pkt.data[6:]
                    CSPlayerInterface_Proxy = proxy_server('%d.%d.%d.%d' % CSPlayerInterfaceAddr[:4], CSPlayerInterfaceAddr[4], 7037)
                    
            elif pkt.sender == "CSPlayerInterface":
                pass
            
            self.read_buffer = self.read_buffer[pkt.size:]      # remove datas of a full packet from the buffer
            
            buffer = pkt.GetBuffer(False)  # Return the full packet from the object
            self.receiver.write_buffer += [buffer]    # Add this packet into the write buffer of the receiver 
            print "%s:%d -> %s:%d  %d bytes" % (self.receiver.server.there[0], self.receiver.server.there[1], self.receiver.addr[0], self.receiver.addr[1], pkt.size)
            print "OpCode : %d" % (pkt.opCode)
            print pkt.data.encode("hex")
            #print buffer.encode("hex")
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
        self.read_buffer += self.recv(4096)
        while self.read_buffer:
            pkt = packet()
            pkt.ReadFromBuffer(self.read_buffer, False)
            
            if pkt.size > len(self.read_buffer):
                break
            
            self.read_buffer = self.read_buffer[pkt.size:]
            
            buffer = pkt.GetBuffer(False)
            self.sender.write_buffer += [buffer]
            print "%s:%d -> %s:%d  %d bytes" % (self.addr[0], self.addr[1], self.server.there[0], self.server.there[1], pkt.size)
            print "OpCode : %d" % (pkt.opCode)
            print pkt.data.encode("hex")
            #print buffer.encode("hex")
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
         
UniverServer = proxy_server('213.244.186.134', 7000, 7000)
asyncore.loop()
