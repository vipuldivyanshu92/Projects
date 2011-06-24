import asyncore
import socket
from SRP6 import SRP6, ValueNotSetException
import convertool
from structures import *

class RealmClient(asyncore.dispatcher):
    def __init__(self, host):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 3724))
        self.writebuffer = []
        self.srp = SRP6(g = 7)
        self.handler = {
            0x00 : self.handleAuthLogonChallenge,
            0x01 : self.handleAuthLogonProof,
            #0x10 : self.handleRealmList,
        }

    def initiateAuthLogonChallenge(self):
        c = Container(
            opcode = 0,
            error = 8,
            size = 30 + len('ADMINISTRATOR'),
            gamename = 'WoW'[::-1],
            version = [3, 1, 3],
            build = 9947,
            platform = 'x86'[::-1],
            os = 'Win'[::-1],
            country = 'frFR'[::-1],
            timezone = 0,
            ip = 2130706433,
            I = 'ADMINISTRATOR'
        )
        r = ST_AUTH_LOGON_CHALLENGE_C.build(c)
        self.writebuffer.append(r)

    def handleAuthLogonChallenge(self, pkt):
        data = ST_AUTH_LOGON_CHALLENGE_S.parse(pkt)
        #print(data)
        self.srp.set_I('ADMINISTRATOR')
        self.srp.set_P('ADMINISTRATOR')
        self.srp.set_B(convertool.strToInt(data.SRP_B[::-1]))
        self.srp.set_g(convertool.strToInt(data.SRP_g[::-1]))
        self.srp.set_N(convertool.strToInt(data.SRP_N[::-1]))
        self.srp.set_s(convertool.strToInt(data.SRP_s[::-1]))
        self.srp.generate_a()
        self.srp.calculate_A()
        self.srp.calculate_x()
        self.srp.calculate_v()
        self.srp.calculate_u()
        self.srp.calculate_S_client()
        self.srp.calculate_K()
        self.srp.calculate_M1()
        self.srp.calculate_M2()

        r = ST_AUTH_LOGON_PROOF_C.build(Container(
            opcode = 1,
            SRP_A = convertool.intToStr(self.srp.get_A())[::-1],
            SRP_M1 = convertool.intToStr(self.srp.get_M1()),
            CRC = chr(0) * 20,
            unk = 0
        ))
        self.writebuffer.append(r)

    def handleAuthLogonProof(self, pkt):
        data = ST_AUTH_LOGON_PROOF_S .parse(pkt)
        #print(data)
        if data.SRP_M2.encode('hex') ==  '%x' % self.srp.get_M2():
            print('M2 Matches !')
        else:
            print('Something goes wrong during authentification :(')

        #Ask for realm enumeration
        self.writebuffer.append('1000000000'.decode('hex'))

    def handle_connect(self):
        self.initiateAuthLogonChallenge()

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

c = RealmClient('127.0.0.1')

asyncore.loop()
