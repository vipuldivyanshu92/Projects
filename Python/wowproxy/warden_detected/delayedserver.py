from commonenv import commonenv
import asyncore
import socket

class SKChannel(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        if data:
            print data
            self.close()
            
    def writable(self):
        return False

class SKServer(asyncore.dispatcher):
    def __init__(self, port=9999):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)
        print("listening on port %d" % (self.port))

    def handle_accept(self):
        channel, addr = self.accept()
        SKChannel(channel)

serv = SKServer()
asyncore.loop()
