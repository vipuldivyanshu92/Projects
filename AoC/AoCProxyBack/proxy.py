#!/usr/bin/env python

import asyncore
import socket
from construct import *
from exttypes import *
from dispatcher import *

class proxy_server(asyncore.dispatcher):
    def __init__(self, remotehost, remoteport, bindport, XMLfiles):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.there = (remotehost, remoteport)
        self.bind(('', bindport))
        self.listen(1)
        self.pkt_dispatcher = dispatcher(XMLfiles)
        print 'Listening on port %d \n' % (bindport)

    def handle_accept(self):
        proxy_receiver(self, self.accept(), self.pkt_dispatcher)


class proxy_receiver(asyncore.dispatcher):
    def __init__(self, server, (sock, addr), pkt_dispatcher):
        asyncore.dispatcher.__init__(self, sock)
        self.server = server
        self.sender = proxy_sender(self, server.there, pkt_dispatcher)
        self.addr = addr
        self.pkt_dispatcher = pkt_dispatcher

        #Definition of buffers
        self.recv_buffer = ''
        self.send_buffer = []

    def handle_connect(self):
        print 'Received incomming connection from %s' % (self.addr[0])

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
                print '[opcode : %d] %s -> %s' % (header.Opcode, header.Sender, header.Receiver)

                if self.pkt_dispatcher.has_opcode(header.Sender, header.Opcode):
                    structure = self.pkt_dispatcher.GetpacketStruct(header.Sender, header.Opcode)
                    
                    if structure.subcons:
                        parsed = True
                        pkt = structure.parse(self.recv_buffer[headersize:header.pktSize+4])

                        overwritemask = self.pkt_dispatcher.GetpacketOverwrite(header.Sender, header.Opcode)
                        if overwritemask:
                            for field in overwritemask:
                                pkt.__setattr__(field, overwritemask[field])
                                
                            #the outpkt only need to be rebuild in this case
                            bpkt = structure.build(pkt)
                            header.pktSize = len(bpkt) + headersize - 4
                            bhead = headerstruct.build(header)
                            outpkt = bhead + bpkt

                    else:
                        print 'No structure defined for packet %s.' % (self.pkt_dispatcher.Getname(header.Sender, header.Opcode))
                else:
                    print 'No packet defined for opcode %d' % (header.Opcode)

                self.sender.send_buffer.append(outpkt)
                self.recv_buffer = self.recv_buffer[fullsize:]

                if parsed:
                    print pkt, '\n'
                else:
                    print outpkt.encode('hex') 
            else:
                break

    def handle_write(self):
        self.send(self.send_buffer.pop(0))

    def handle_close(self):
        print 'Closing connection from %s' % (self.addr[0])
        self.sender.close()
        self.close()

    
class proxy_sender (asyncore.dispatcher):
    def __init__ (self, receiver, address, pkt_dispatcher):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(address)
        self.there = address
        self.pkt_dispatcher = pkt_dispatcher

        #Definition of buffers
        self.recv_buffer = ''
        self.send_buffer = []

    def handle_connect (self):
        print 'Connected to %s:%d\n' % self.there
        
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
                print '[opcode : %d] %s -> %s' % (header.Opcode, header.Sender, header.Receiver)

                if self.pkt_dispatcher.has_opcode(header.Sender, header.Opcode):
                    structure = self.pkt_dispatcher.GetpacketStruct(header.Sender, header.Opcode)
                    
                    if structure.subcons:
                        parsed = True
                        pkt = structure.parse(self.recv_buffer[headersize:header.pktSize+4])

                        overwritemask = self.pkt_dispatcher.GetpacketOverwrite(header.Sender, header.Opcode)
                        if overwritemask:
                            for field in overwritemask:
                                pkt.__setattr__(field, overwritemask[field])
                                
                            #the outpkt only need to be rebuild in this case
                            bpkt = structure.build(pkt)
                            header.pktSize = len(bpkt) + headersize - 4
                            bhead = headerstruct.build(header)
                            outpkt = bhead + bpkt

                    else:
                        print 'No structure defined for packet %s.' % (self.pkt_dispatcher.Getname(header.Sender, header.Opcode))
                else:
                    print 'No packet defined for opcode %d' % (header.Opcode)

                self.receiver.send_buffer.append(outpkt)
                self.recv_buffer = self.recv_buffer[fullsize:]

                if parsed:
                    print pkt, '\n'
                else:
                    print outpkt.encode('hex') 
            else:
                break
            
    def handle_write(self):
        self.send(self.send_buffer.pop(0))

    def handle_close (self):
        print 'closing connection to %s:%d' % self.there
        self.receiver.close()
        self.close()

Universe = proxy_server('213.244.186.134', 7000, 7000, ['UniverseInterface.xml', 'UniverseAgent.xml'])
asyncore.loop()
