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
import sys
import os
import logging
from construct import *
from exttypes import *
from dispatcher import *

class proxy_server(asyncore.dispatcher):
    def __init__(self, remotehost, remoteport, bindport, XMLfiles, LOGfile):
        asyncore.dispatcher.__init__(self)

        # Creation of the local logger
        handler = logging.FileHandler(LOGfile)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        loggername = os.path.splitext(LOGfile)[0]
        logging.getLogger(loggername).addHandler(handler)
        self.logger = logging.getLogger(loggername)

        # Creation of the Socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.there = (remotehost, remoteport)
        self.bind(('', bindport))
        self.set_reuse_addr()
        self.listen(1)
        self.pkt_dispatcher = dispatcher(XMLfiles)

        self.logger.info('Listening on port %d \n' % (bindport))

    def handle_accept(self):
        proxy_receiver(self, self.accept(), self.pkt_dispatcher, self.logger)


class proxy_receiver(asyncore.dispatcher):
    def __init__(self, server, (sock, addr), pkt_dispatcher, logger):
        asyncore.dispatcher.__init__(self, sock)
        self.logger = logger
        self.server = server
        self.sender = proxy_sender(self, server.there, pkt_dispatcher, logger)
        self.addr = addr
        self.pkt_dispatcher = pkt_dispatcher

        #Definition of buffers
        self.recv_buffer = ''
        self.send_buffer = []

    def handle_connect(self):
        self.logger.info('Received incomming connection from %s' % (self.addr[0]))

    def handle_expt(self):
        self.close()

    def writable(self):
        return len(self.send_buffer) > 0

    def handle_read(self):
        self.recv_buffer += self.recv(4096)
        
        while self.recv_buffer:
            headerstruct = self.pkt_dispatcher.GetheaderStruct()
            header = headerstruct.parse(self.recv_buffer)

            if header.pktSize + 4 <= self.recv_buffer:
                parsed = False
                headersize = 28 + len(header.Sender) + len(header.Receiver)
                fullsize = header.pktSize + 4
                outpkt = self.recv_buffer[:header.pktSize+4]
                self.logger.info('[opcode : %d] %s -> %s' % (header.Opcode, header.Sender, header.Receiver))

                if self.pkt_dispatcher.has_opcode(header.Sender, header.Opcode):
                    structure = self.pkt_dispatcher.GetpacketStruct(header.Sender, header.Opcode)
                    
                    if structure.subcons:
                        parsed = True
                        pkt = structure.parse(self.recv_buffer[headersize:header.pktSize+4])

                        overwritemask = self.pkt_dispatcher.GetpacketOverwrite(header.Sender, header.Opcode)
                        if overwritemask:
                            for field in overwritemask:
                                pkt.__setattr__(field, type(pkt.__getattribute__(field))(overwritemask[field]))
                                
                            #the outpkt only need to be rebuild in this case
                            bpkt = structure.build(pkt)
                            header.pktSize = len(bpkt) + headersize - 4
                            bhead = headerstruct.build(header)
                            outpkt = bhead + bpkt

                    else:
                        self.logger.info('No structure defined for packet %s.' % (self.pkt_dispatcher.Getname(header.Sender, header.Opcode)))
                else:
                    self.logger.info('No packet defined for opcode %d' % (header.Opcode))

                self.sender.send_buffer.append(outpkt)
                self.recv_buffer = self.recv_buffer[fullsize:]

                if parsed:
                    self.logger.info(str(pkt) + '\n')
                else:
                    self.logger.info(outpkt.encode('hex') + '\n')
            else:
                break

    def handle_write(self):
        self.send(self.send_buffer.pop(0))

    def handle_close(self):
        self.logger.info('Closing connection from %s' % (self.addr[0]))
        self.sender.close()
        self.close()

    
class proxy_sender (asyncore.dispatcher):
    def __init__ (self, receiver, address, pkt_dispatcher, logger):
        asyncore.dispatcher.__init__(self)
        self.logger = logger
        self.receiver = receiver
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(address)
        self.there = address
        self.pkt_dispatcher = pkt_dispatcher

        #Definition of buffers
        self.recv_buffer = ''
        self.send_buffer = []

    def handle_connect (self):
        self.logger.info('Connected to %s:%d\n' % self.there)
        
    def handle_expt(self):
        self.close()

    def writable(self):
        return len(self.send_buffer) > 0

    def handle_read(self):
        self.recv_buffer += self.recv(4096)
        
        while self.recv_buffer:
            headerstruct = self.pkt_dispatcher.GetheaderStruct()
            header = headerstruct.parse(self.recv_buffer)

            if header.pktSize + 4 <= self.recv_buffer:
                parsed = False
                headersize = 28 + len(header.Sender) + len(header.Receiver)
                fullsize = header.pktSize + 4
                outpkt = self.recv_buffer[:header.pktSize+4]
                self.logger.info('[opcode : %d] %s -> %s' % (header.Opcode, header.Sender, header.Receiver))

                if self.pkt_dispatcher.has_opcode(header.Sender, header.Opcode):
                    structure = self.pkt_dispatcher.GetpacketStruct(header.Sender, header.Opcode)
                    
                    if structure.subcons:
                        parsed = True
                        pkt = structure.parse(self.recv_buffer[headersize:header.pktSize+4])

                        if header.Opcode == 1 and header.Sender == 'UniverseInterface':
                            TerritoryMgrAddr = pkt.TerritoryManagerAddr.split(':')
                            TerritoryMgr = proxy_server(TerritoryMgrAddr[0] , int(TerritoryMgrAddr[1]), 7001, ['PlayerInterface.xml', 'PlayerAgent.xml'], 'TerritoryManager.log')

                        if header.Opcode == 3 and header.Sender == 'PlayerInterface':
                            CSServer = proxy_server('%d.%d.%d.%d' % (pkt.CSServerAddr1, pkt.CSServerAddr2, pkt.CSServerAddr3, pkt.CSServerAddr4), pkt.CSServerPort, 7002, ['CSPlayerAgent.xml', 'CSPlayerInterface.xml'], 'CSServer.log')

                        overwritemask = self.pkt_dispatcher.GetpacketOverwrite(header.Sender, header.Opcode)
                        if overwritemask:
                            for field in overwritemask:
                                pkt.__setattr__(field, type(pkt.__getattribute__(field))(overwritemask[field]))
                                
                            #the outpkt only need to be rebuild in this case
                            bpkt = structure.build(pkt)
                            header.pktSize = len(bpkt) + headersize - 4
                            bhead = headerstruct.build(header)
                            outpkt = bhead + bpkt

                    else:
                        self.logger.info('No structure defined for packet %s.' % (self.pkt_dispatcher.Getname(header.Sender, header.Opcode)))
                else:
                    self.logger.info('No packet defined for opcode %d' % (header.Opcode))

                self.receiver.send_buffer.append(outpkt)
                self.recv_buffer = self.recv_buffer[fullsize:]

                if parsed:
                    self.logger.info(str(pkt) + '\n')
                else:
                    self.logger.info(outpkt.encode('hex') + '\n')
            else:
                break
            
    def handle_write(self):
        self.send(self.send_buffer.pop(0))

    def handle_close (self):
        self.logger.info('closing connection to %s:%d' % self.there)
        self.receiver.close()
        self.close()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

Universe = proxy_server('213.244.186.134', 7000, 7000, ['UniverseInterface.xml', 'UniverseAgent.xml'], 'Universe.log')

asyncore.loop()
