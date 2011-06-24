import asyncore
import socket
from construct import *
import convertool
from world_structures import *
from database import db
from config import config
from world_crypto import WorldCrypto
# From s->c size (2bytes), opcode (2bytes)
# From c->s size (2bytes), opcode (4bytes)

class WorldChannel(asyncore.dispatcher):
    def __init__(self, sock, env):
        asyncore.dispatcher.__init__(self, sock)
        self.env = env
        self.recvbuffer = ''
        self.encrypted = False
        self.header = None
        self.writebuffer = ['000000000006EC013669F7C2'.decode('hex')]
        self.handler = {
            #0x01ED : 
        }

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        self.recvbuffer += data
        while len(self.recvbuffer) >= 6:
            if not self.header:
                if self.encrypted:
                    pass
                    #self.header = Header_struct.parse(RC4.stuff(self.recvbuffer[:6]))
                else:
                    self.header = CLIENT_HEADER_STRUCT.parse(self.recvbuffer[:6])
                
            # +2 for the size of the size itself
            if self.header.size+2 <= len(self.recvbuffer):
                # We have a packet
                pkt = self.recvbuffer[6:self.header.size+2]
                self.recvbuffer = self.recvbuffer[self.header.size+2:]
                print('OPCODE : %d' % (self.header.opcode))
                print('SIZE : %d' % (self.header.size))
                print(convertool.strToProperHex(pkt))
                if self.header.opcode in self.handler:
                    self.handler[opcode](pkt)
                else:
                    print('packet not handled %d' % self.header.opcode)
                self.header = None
                    
            else:
                # packet is not yet complete
                break

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)
            print('P>C SENT %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))    


# Listen for incoming connections
class WorldServer(asyncore.dispatcher):
    def __init__(self, port=8085):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)
        print("listening on port %d\n" % (self.port))

    def handle_accept(self):
        channel, addr = self.accept()
        env = dict()  # environment, the link between client and server of the proxy
        env['client'] = None
        env['server'] = WorldChannel(channel, env)
