import asyncore
import socket
import threading
from SRP6 import SRP6, ValueNotSetException
import convertool
from realm_structures import *
from database import db
from config import config

class RealmClient(asyncore.dispatcher):
    def __init__(self, host, port, env):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.env = env
        self.connect((host, port))
        self.writebuffer = []
        self.srp = SRP6(g = 7)
        self.handler = {
            0x00 : self.handleAuthLogonChallenge,
            0x01 : self.handleAuthLogonProof,
            0x10 : self.handleRealmList,
        }

    def initAuthentification(self):
        self.initiateAuthLogonChallenge()

    def initiateAuthLogonChallenge(self):
        # Retrieve data from config
        cversion = [int(i) for i in config.get('GLOBAL', 'version').split('.')]
        cbuild = config.getint('GLOBAL', 'build')
        cplatform = config.get('GLOBAL', 'platform')
        cos = config.get('GLOBAL', 'os')
        ccountry = config.get('GLOBAL', 'country')
        
        c = Container(
            opcode = 0,
            error = 8,
            size = 30 + len(self.env['username']),
            gamename = 'WoW'[::-1],
            version = cversion,
            build = cbuild,
            platform = cplatform[::-1],
            os = cos[::-1],
            country = ccountry[::-1],
            timezone = 0,
            ip = 2130706433,            #127.0.0.1
            I = self.env['username']
        )
        r = ST_AUTH_LOGON_CHALLENGE_C.build(c)
        self.writebuffer.append(r)

    def handleAuthLogonChallenge(self, pkt):
        data = ST_AUTH_LOGON_CHALLENGE_S.parse(pkt)
        #print(data)
        self.srp.set_I(self.env['username'])
        self.srp.set_P(self.env['userpass'])
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

        # Store the sessionkey in the DB
        cursor = db.cursor()
        cursor.execute('UPDATE accounts SET client_K = ? WHERE username = ?', [convertool.intToHex(self.srp.get_K(), 80), self.env['username']])
        db.commit()

        r = ST_AUTH_LOGON_PROOF_C.build(Container(
            opcode = 1,
            SRP_A = convertool.intToStr(self.srp.get_A())[::-1],
            SRP_M1 = convertool.intToStr(self.srp.get_M1()),
            CRC = chr(0) * 20,      # don't know how to calculate it
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

    def handleRealmList(self, pkt):
        self.env['condition'].acquire()

        realms = ST_REALM_LIST_S_FULL.parse(pkt)
        self.env['realms'] = dict([[r.name, r] for r in realms.Realm])
        
        self.env['condition'].notify()
        self.env['condition'].release()

    def handle_connect(self):
        pass

    def handle_read(self):
        data = self.recv(4096)
        if data:
            print('S>P RECEIVED %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))
            opcode = ord(data[0])
            if opcode in self.handler:
                self.handler[opcode](data)

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)
            print('P>S SENT %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))

class RealmChannel(asyncore.dispatcher):
    def __init__(self, sock, env):
        asyncore.dispatcher.__init__(self, sock)
        self.env = env
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

        # Get database cursor
        cursor = db.cursor()

        # Set the username in the env
        self.env['username'] = data.I
        self.env['userpass'] = cursor.execute('SELECT password FROM accounts WHERE username = ?', [data.I]).fetchone()[0]   # not safe should do some checking

        # Do client part authentification
        self.env['client'].initAuthentification()
        
        # Init SRP Object
        self.srp.set_I(data.I)
        self.srp.set_P(self.env['userpass'])
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

        # Store the sessionkey in the DB
        cursor = db.cursor()
        cursor.execute('UPDATE accounts SET server_K = ? WHERE username = ?', [convertool.intToHex(self.srp.get_K(), 80), self.env['username']])
        db.commit()

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
        if not self.env['m_realms']:
            self.env['condition'].acquire()
            while not self.env['realms']:
                self.env['condition'].wait()

            # Retrieve the realm address
            cursor = db.cursor()
            rn = cursor.execute('SELECT realm_name FROM accounts WHERE username = ?', [self.env['username']]).fetchone()[0] # not safe
            rn = rn.encode('latin-1') # maybe realms name are in unicode need to check
            cursor.execute('UPDATE accounts SET realm_address = ? WHERE username = ?', [self.env['realms'][rn].address, self.env['username']])
            db.commit()
            # Alter it and send the altered version
            m_realms = self.env['realms']
            m_realms[rn].address = '127.0.0.1:8085'     # need to change to the proxy address
            m_realms[rn].name += ' - PROXY'
            c = Container(
                unk1 = 0,
                nb_realms = len(m_realms),
                Realm = m_realms.values(),
                unk2 = 0x10,
                unk3 = 0
            )
            pkt_p = ST_REALM_LIST_S_PAYLOAD.build(c)
            c = Container(
                opcode = 0x10,
                size = len(pkt_p)
            )
            pkt_h = ST_REALM_LIST_S_HEADER.build(c)
            self.env['m_realms'] = pkt_h + pkt_p
            
            self.env['condition'].release()
            
        self.writebuffer.append(self.env['m_realms'])

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        if data:
            print('C>P RECEIVED %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))
            opcode = ord(data[0])
            if opcode in self.handler:
                self.handler[opcode](data)

    def handle_write(self):
        if self.writebuffer:
            data = self.writebuffer.pop(0)
            self.send(data)
            print('P>C SENT %d bytes:' % (len(data)))
            print(convertool.strToProperHex(data))    


# Listen for incoming connections
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
        env = dict()  # environment, the link between client and server of the proxy
        env['condition'] = threading.Condition()        # don't know if it's a good way to do it
        env['realms'] = None
        env['m_realms'] = None
        env['client'] = RealmClient('127.0.0.1', 37240, env)
        env['server'] = RealmChannel(channel, env)
