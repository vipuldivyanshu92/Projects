import asyncore, socket

# Connection PROXY <> SERVER
class WorldClient(asyncore.dispatcher):
    def __init__(self, host, port, env):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.env = env
        self.connect((host, port))
        self.writebuffer = []

    def write(self, data):
        self.writebuffer.append(data)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        if data:
            self.env['server'].write(data)

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

    def write(self, data):
        self.writebuffer.append(data)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        if data:
            self.env['client'].write(data)

    def writable(self):
        return len(self.writebuffer) > 0

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)

class WorldProxy(asyncore.dispatcher):
    port = 8085
    
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        port = WorldProxy.port
        WorldProxy.port += 1
        self.bind(('', port))
        self.listen(1)
        print("listening on port %d" % (port))

    def handle_accept(self):
        channel, addr = self.accept()
        self.env = dict()
        self.env['server'] = RealmChannel(channel, self.env)

    def initClient(self):
        self.env['client'] = RealmClient(self.rhost, self.rport, self.env)

s1 = WorldProxy()
s2 = WorldProxy()
asyncore.loop()
