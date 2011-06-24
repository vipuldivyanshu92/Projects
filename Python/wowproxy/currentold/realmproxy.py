import asyncore, socket

# Connection PROXY <> SERVER
class RealmClient(asyncore.dispatcher):
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
class RealmChannel(asyncore.dispatcher):
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

class RealmServer(asyncore.dispatcher):
    def __init__(self, lport, rhost, rport):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rhost = rhost
        self.rport = rport
        self.bind(("", lport))
        self.listen(5)
        print("listening on port %d" % (lport))

    def handle_accept(self):
        channel, addr = self.accept()
        env = dict()
        env['client'] = RealmClient(self.rhost, self.rport, env)
        env['server'] = RealmChannel(channel, env)

r = RealmServer(3724, 'www.avalonserver.org', 3725)
asyncore.loop()
