from construct import *
from errors import *
import packet
import asyncore
import socket
import zlib

class server(asyncore.dispatcher):
    def __init__(self, port, nb_conn, handler, zcompress):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(nb_conn)
        self.handler = handler
        
        self.zcompress = zcompress
                
        self.packetMgr = {}
        
    def handle_accept(self):
        (conn_sock, client_addr) = self.accept()
        self.handler(conn_sock, client_addr, self)
        
    def handle_close(self):
        self.close()
        
class GlobalHandler(asyncore.dispatcher):
    
    global BUFFER_SIZE
    BUFFER_SIZE = 4096
       
    def __init__(self, conn_sock, client_addr, server):
        asyncore.dispatcher.__init__(self, conn_sock)
        # Saving server reference
        self.server = server
        
        # Defining the socket informations
        self.conn_sock = conn_sock
        self.client_addr = client_addr
        
        # Defining Buffers
        self.read_buffer = ""
        self.write_buffer = []
        
        # Creating zlibs objects if necessary
        self.DecompressObj = zlib.decompressobj()
        self.CompressObj = zlib.compressobj()
        self.read_firsttime = False
        self.write_firsttime = False
        
        # Logging informations
        print "Handler created for socket %d at %s:%d" % (id(conn_sock), client_addr[0], client_addr[1])
        
    def ReadPacket(self):
        """
            Get the size, if the size is too short raise an exception
            else return a packet structure (construct lib).
        """
        try:
            size = UBInt32("size").parse(self.read_buffer)
            if len(self.read_buffer) >= size:
                pkt = packet.PACKET_STRUCT.parse(self.read_buffer)
                self.read_buffer = self.read_buffer[pkt.size + 4:]
                return pkt
        except:
            raise PacketReadError          
        
    def handle_read(self):
        
        s = self.recv(BUFFER_SIZE)
        
        if self.server.zcompress:
            if not self.read_firsttime:
                s = self.DecompressObj.decompress(s[5:])
                self.read_firsttime = True
            else:
                s = self.DecompressObj.decompress(s)
        
        self.read_buffer += s

        while self.read_buffer:
            try:
                pkt = self.ReadPacket()
                if pkt.opcode in self.server.packetMgr[pkt.sender]:
                    self.server.packetMgr[pkt.sender][pkt.opcode](self, pkt)
                else:
                    print "not handled packet : %d from : %s" % (pkt.opcode, pkt.sender)
                
            except PacketReadError:
                break
        
    def handle_write(self):
        #if self.server.zcompress:
        #    if not self.write_firsttime:
        #        print "here"
        #        self.send(self.CompressObj.compress("8000000100".decode("hex") + self.write_buffer.pop(0)))
        #        self.write_firsttime = True
        #    else:
        #        self.send(self.CompressObj.compress(self.write_buffer.pop(0)))
        #else:
        self.send(self.write_buffer.pop(0))
    
    def writable(self):
        return len(self.write_buffer) > 0
    
    def handle_close(self):
        print "Handler closed for socket %d at %s:%d" % (id(self.conn_sock), self.client_addr[0], self.client_addr[1])
        self.close()