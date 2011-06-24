import asyncore
import socket

class KeyChannel(asyncore.dispatcher):
    def __init__(self, sock, env):
        asyncore.dispatcher.__init__(self, sock)
        self.env = env

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        self.env['key'] = data.decode('hex')
        self.close()
        
    def writable(self):
        pass

class KeyServer(asyncore.dispatcher):
    def __init__(self, port, env):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.env = env
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)
        print("listening on port %d" % (self.port))

    def handle_accept(self):
        channel, addr = self.accept()
        KeyChannel(channel, self.env)
