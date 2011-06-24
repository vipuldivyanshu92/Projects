import asyncore, socket
import logging
from construct import *
from worldcrypto import WorldCrypto
import convertool

# filters
from filters import chatFilter

CLIENT_HEADER_STRUCT = Struct('CLIENT_HEADER_STRUCT',
    UBInt16('size'),
    ULInt32('opcode')
)

SERVER_HEADER_STRUCT = Struct('SERVER_HEADER_STRUCT',
    UBInt16('size'),
    ULInt16('opcode')
)

# Connection PROXY <> SERVER
class WorldClient(asyncore.dispatcher):
    def __init__(self, host, port, env):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.env = env
        self.connect((host, port))
        self.writebuffer = []
        self.recvbuffer = ''
        self.header = None
        self.encrypted = False
        self.crypt = None
        self.handler = {
            150 : chatFilter.chatFilter
        }

    def write(self, data):
        head = CLIENT_HEADER_STRUCT.build(data[0])
        if self.encrypted:
            head = self.crypt.encrypt(head)
        self.writebuffer.append(head + data[1])

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        self.recvbuffer += data
        while len(self.recvbuffer) >= 4:
            if not self.header:
                if self.encrypted:
                    self.header = SERVER_HEADER_STRUCT.parse(self.crypt.decrypt(self.recvbuffer[:4]))
                else:
                    self.header = SERVER_HEADER_STRUCT.parse(self.recvbuffer[:4])
                
            # +2 for the size of the size itself
            if self.header.size+2 <= len(self.recvbuffer):
                # We have a packet
                pkt = self.recvbuffer[4:self.header.size+2]
                self.recvbuffer = self.recvbuffer[self.header.size+2:]
                logging.info('OPCODE : %d\nSIZE : %d' % (self.header.opcode, self.header.size))
                logging.debug('RECEIVED:\n' + convertool.strToProperHex(pkt))
                if self.header.opcode in self.handler:
                    self.handler[self.header.opcode](pkt, self.env)
                    
                self.env['world']['server'].write((self.header, pkt))
                self.header = None
                    
            else:
                # packet is not yet complete
                break

    def writable(self):
        return len(self.writebuffer) > 0

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)

# Connection CLIENT <> PROXY
class WorldChannel(asyncore.dispatcher):
    def __init__(self, sock, env):
        asyncore.dispatcher.__init__(self, sock)
        self.env = env
        self.writebuffer = []
        self.recvbuffer = ''
        self.header = None
        self.encrypted = False
        self.crypt = None
        self.handler = {
        }

    def write(self, data):
        head = SERVER_HEADER_STRUCT.build(data[0])
        if self.encrypted:
            head = self.crypt.encrypt(head)
        self.writebuffer.append(head + data[1])

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
                    self.header = CLIENT_HEADER_STRUCT.parse(self.crypt.decrypt(self.recvbuffer[:6]))
                else:
                    self.header = CLIENT_HEADER_STRUCT.parse(self.recvbuffer[:6])
                
            # +2 for the size of the size itself
            if self.header.size+2 <= len(self.recvbuffer):
                # We have a packet
                pkt = self.recvbuffer[6:self.header.size+2]
                self.recvbuffer = self.recvbuffer[self.header.size+2:]
                logging.info('OPCODE : %d\nSIZE : %d' % (self.header.opcode, self.header.size))
                logging.debug('SENT:\n' + convertool.strToProperHex(pkt))
                if self.header.opcode in self.handler:
                    self.handler[self.header.opcode](pkt, self.env)
                    
                self.env['world']['client'].write((self.header, pkt))
                if self.header.opcode == 493:
                    self.encrypted = True
                    self.crypt = WorldCrypto(self.env['key'], 'server')
                    self.env['world']['client'].encrypted = True
                    self.env['world']['client'].crypt = WorldCrypto(self.env['key'], 'client')
                self.header = None
                    
            else:
                # packet is not yet complete
                break

    def writable(self):
        return len(self.writebuffer) > 0

    def handle_write(self):
        if self.writebuffer and self.env['key']:
            data = self.writebuffer.pop(0)
            self.send(data)    

class WorldServer(asyncore.dispatcher):
    def __init__(self, lport, rhost, rport, env):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rhost = rhost
        self.rport = rport
        self.env = env
        self.bind(("", lport))
        self.listen(5)
        print("listening on port %d" % (lport))

    def handle_accept(self):
        channel, addr = self.accept()
        self.env['world']['client'] = WorldClient(self.rhost, self.rport, self.env)
        self.env['world']['server'] = WorldChannel(channel, self.env)
