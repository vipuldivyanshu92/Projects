import asyncore, socket
from construct import *
from config import config

# Connection PROXY <> SERVER
class RealmClient(asyncore.dispatcher):
    def __init__(self, host, port, env):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.env = env
        self.connect((host, port))
        self.writebuffer = []
        self.recvbuffer = ''
        self.readhandler = {
            0x10 : self.handleRealmList
        }

    def write(self, data):
        self.writebuffer.append(data)

    def handleRealmList(self, data):
        ST_REALM = Struct('Realm',
                ULInt8('icon'),
                ULInt8('lock'),
                ULInt8('color'),
                CString('name'),
                CString('address'),
                LFloat32('population'),
                ULInt8('nb_characters'),
                ULInt8('timezone'),
                ULInt8('unk')
        )

        ST_REALM_LIST_S_HEADER = Struct('REALM_LIST_S_HEADER',
            ULInt8('opcode'),
            ULInt16('size')
        )

        ST_REALM_LIST_S_PAYLOAD = Struct('REALM_LIST_S',
            ULInt32('unk1'),
            ULInt16('nb_realms'),
            Array(lambda ctx: ctx['nb_realms'], ST_REALM),
            ULInt8('unk2'),
            ULInt8('unk3')
        )

        ST_REALM_LIST_S_FULL = Struct('REALM_LIST_S',
            Embed(ST_REALM_LIST_S_HEADER),
            Embed(ST_REALM_LIST_S_PAYLOAD)
        )

        try:
            realms = ST_REALM_LIST_S_FULL.parse(data)
            realmsList = realms.Realm
        except:
            return None

        if len(data)-3 < realms.size:
            return None
        
        for r in realmsList:
            r.address = '%s:%s' % (config.get('GLOBAL', 'proxyhost'), config.get('WORLD', 'localport'))
            r.name += ' - PROXY'

        c = Container(
            unk1 = 0,
            nb_realms = len(realmsList),
            Realm = realmsList,
            unk2 = 0x10,
            unk3 = 0
        )
        pkt_p = ST_REALM_LIST_S_PAYLOAD.build(c)
        c = Container(
            opcode = 0x10,
            size = len(pkt_p)
        )
        pkt_h = ST_REALM_LIST_S_HEADER.build(c)

        return pkt_h + pkt_p

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        self.recvbuffer += self.recv(4096)
        if self.recvbuffer:
            if ord(self.recvbuffer[0]) in self.readhandler:
                data = self.readhandler[ord(self.recvbuffer[0])](self.recvbuffer)
            else:
                data = self.recvbuffer
            if data:
                self.env['realm']['server'].write(data)
                self.recvbuffer = self.recvbuffer[len(data):]

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
            self.env['realm']['client'].write(data)

    def writable(self):
        return len(self.writebuffer) > 0

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)    

class RealmServer(asyncore.dispatcher):
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
        self.env['realm']['client'] = RealmClient(self.rhost, self.rport, self.env)
        self.env['realm']['server'] = RealmChannel(channel, self.env)
