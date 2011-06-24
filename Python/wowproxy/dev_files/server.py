import asyncore
import socket
from SRP6 import SRP6, ValueNotSetException
import convertool
from structures import *

class RealmChannel(asyncore.dispatcher):
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        self.srp = SRP6(g = 7, N = int('894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7', 16))
        self.writebuffer = []
        self.handler = {
            0x00 : self.handleAuthLogonChallenge,
            0x01 : self.handleAuthLogonProof,
            0x10 : self.handleRealmList,
        }

    def handleAuthLogonChallenge(self, pkt):
        data = ST_AUTH_LOGON_CHALLENGE_C.parse(pkt)
        #print(data)
        # Init SRP Object
        self.srp.set_I(data.I)
        self.srp.set_P('ADMINISTRATOR')
        self.srp.generate_b()
        self.srp.generate_s()
        self.srp.calculate_x()
        self.srp.calculate_v()
        self.srp.calculate_B()

        # Create the response packet
        r = ST_AUTH_LOGON_CHALLENGE_S.build(Container(
            opcode = 0,
            unk = 0,
            error = 0,
            SRP_B = convertool.intToStr(self.srp.get_B())[::-1],
            SRP_g = chr(self.srp.get_g()),
            SRP_N = convertool.intToStr(self.srp.get_N())[::-1],
            SRP_s = convertool.intToStr(self.srp.get_s())[::-1],
            CRC_salt = '430d7525f492e4e03bc66b8d1130cfac'.decode('hex'),
            security_flag = 0
        ))
        self.writebuffer.append(r)

    def handleAuthLogonProof(self, pkt):
        data = ST_AUTH_LOGON_PROOF_C.parse(pkt)
        #print(data)
        self.srp.set_A(convertool.strToInt(data.SRP_A[::-1]))
        self.srp.calculate_u()
        self.srp.calculate_S_server()
        self.srp.calculate_K()
        self.srp.calculate_M1()
        self.srp.calculate_M2()

        # Check for authentification correctness
        if data.SRP_M1.encode('hex') == '%x' % self.srp.get_M1():
            print('M1 Matches !')
        else:
            print('Something goes wrong during authentification :(')

        # Create the response packet
        r = ST_AUTH_LOGON_PROOF_S.build(Container(
            opcode = 01,
            error = 0,
            SRP_M2 = convertool.intToStr(self.srp.get_M2()),
            unk1 = 0x00800000,
            unk2 = 0,
            unk3 = 0
        ))
        self.writebuffer.append(r)

    def handleRealmList(self, pkt):
        pass

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(1024)
        if data:
            print('RECEIVED %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))
            opcode = ord(data[0])
            if opcode in self.handler:
                self.handler[opcode](data)

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)
            print('SENT %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))            

class RealmServer(asyncore.dispatcher):
    def __init__(self, port=3724):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)
        print("listening on port %d\n" % (self.port))

    def handle_accept(self):
        channel, addr = self.accept()
        RealmChannel(channel)

server = RealmServer()
asyncore.loop()
