from commonenv import commonenv
import asyncore
import socket
import time

class SKChannel(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        self.timer = 0.0
        self.starttime = time.time()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        if data:
            print data
        
    def writable(self):
        pass

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

s = SKServer()
asyncore.loop()
