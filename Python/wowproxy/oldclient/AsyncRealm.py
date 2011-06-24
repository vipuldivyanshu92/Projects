# Import required librairies
import asyncore
import socket
import struct
import hashlib
import random
import sys
from SharedFunc import *
from Realm_OpCodes import *
from Realm_Structures import *
from Realm_Errors import *


class RealmHandler(asyncore.dispatcher):
    def __init__(self, realmaddress, username, password):       # Parameters for the connection
        self.username = username.upper()                        # Set the Username and password for next packets
        self.password = password.upper()                        # password
        asyncore.dispatcher.__init__(self)                      # Overload the previous definition
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the sock_stream socket
        self.connect((realmaddress, 3724))                      # Connect to the realm_server
        self.buffer = ''                                        # Init the data to send buffer

        self.packethandler = {                                  # Dictionnary with received opcode and function to call
            0x00 : self.SS_AUTH_LOGON_CHALLENGE,
            0x01 : self.SS_AUTH_LOGON_PROOF,
            0x10 : self.SS_REALM_LIST,
            0xFF : self.SS_UNKNOWN,
        }

    def CS_AUTH_LOGON_CHALLENGE(self):
        ulen = len(self.username)
        data = struct.pack(
            ST_AUTH_LOGON_CHALLENGE[0]+"%ds" % (ulen),          # Modify the structure with respect to the username
            OP_AUTH_LOGON_CHALLENGE,                            # OpCode
            0x08, #(changed in 3.1 was 7                        # Error Code
            struct.calcsize(ST_AUTH_LOGON_CHALLENGE[0])-4+ulen, # Packet length
            "WoW",                                              # Game ID
            0x03,                                               # Version[1]
            0x01,                                               # Version[2]
            0x03,                                               # Version[3]
            9947,                                               # Build                 Note : String must be reverse cause of less endian in blizz packets
            "68x",                                              # Platform
            "niW",                                              # Operating System
            "RFrf",                                             # Language
            0x00,                                               # Timezone
            192,                                                # IP[1]
            168,                                                  # IP[2]
            1,                                                  # IP[3]
            4,                                                  # IP[4]
            ulen,                                               # Account Name length
            self.username,                                      # Account Name
        )
        self.buffer += data

    def SS_AUTH_LOGON_CHALLENGE(self, data):
        #print "Auth Logon challenge"
        error = ord(data[2])                        # Get the error value
        if error != 0:                              # 0 Is success
            print ER_AUTH_LOGON_CHALLENGE[error]    # Print error message
            self.close()
            sys.exit()                              # Exit the program

        # Handle the response to the previous packet if no errors
        struct_data = struct.unpack(ST_AUTH_LOGON_CHALLENGE[1], data)

        # Allocate variables for the received values needed for the SRP6 authentification
        SRP_b = struct_data[3]
        SRP_g = struct_data[5]
        SRP_n = struct_data[7]
        SRP_k = 3                                   # k is a constant equal to 3 by default in SRP6 protocol
        SRP_salt = struct_data[8]

        # Generate SRP6 authentifications keys
        ## Generate SRP_A
        SRP_a = random.getrandbits(152)                                     # Get a random value of 19 bytes
        #SRP_a = int('9831C5304B96AC481353D5CE45A3DE119BC9A1', 16)           # Short circuit the random value
        #print "%x" % SRP_a
        SRP_A = IntToStr(modexp(SRP_g, SRP_a, StrToInt(SRP_n[::-1])))[::-1] # Here n is reversed

        ## Generate SRP_x
        SRP_authstr = '%s:%s' % (self.username, self.password)              # Concatenate USER:PASS
        SRP_userhash = hashlib.sha1(SRP_authstr.upper()).digest()           # Get the SHA hash
        SRP_x = hashlib.sha1(SRP_salt+SRP_userhash).digest()[::-1]          # Get SHA of salted user hash

        ## Generate SRP_v
        SRP_v = modexp(SRP_g, StrToInt(SRP_x), StrToInt(SRP_n[::-1]))       # G is 7 in default SRP6 protocol and n is still reversed

        ## Generate SRP_u
        SRP_u = hashlib.sha1(SRP_A+SRP_b).digest()[::-1]    # A is reversed

        ## Generate SRP_S
        SRP_S = modexp(StrToInt(SRP_b[::-1]) - SRP_k*SRP_v, SRP_a + StrToInt(SRP_u) * StrToInt(SRP_x), StrToInt(SRP_n[::-1]))

        ## Generate SRP_SK / Session Key
        SRP_S1 = ""
        SRP_S2 = ""
        tmp_S = IntToStr(SRP_S)[::-1]       # SRP_S is reversed
        for i in range(32):                 # Split the S value in S1 and S2, interleaving each char
           if i % 2 == 0:
              SRP_S1 += tmp_S[i]
           else:
              SRP_S2 += tmp_S[i]
              
        SRP_S1hash = hashlib.sha1(SRP_S1).digest()      # Calculate SHA hash
        SRP_S2hash = hashlib.sha1(SRP_S2).digest()

        SRP_SKhash = ""
        for i in range(20):
           SRP_SKhash += SRP_S1hash[i] + SRP_S2hash[i]  # Join S1hash and S2hash in one string, interleaving each char

        ## Generate M1
        SRP_nhash = hashlib.sha1(SRP_n).digest()                                    # Calculates hashes of previous values
        SRP_ghash = hashlib.sha1(chr(SRP_g)).digest()
        SRP_userhash = hashlib.sha1(self.username).digest()

        SRP_nghash = ""
        for i in range(20):                                                         # Xor n and g
            SRP_nghash += chr(ord(SRP_nhash[i]) ^ ord(SRP_ghash[i]))

        SRP_M1 = hashlib.sha1(SRP_nghash + SRP_userhash + SRP_salt + SRP_A + SRP_b + SRP_SKhash).digest()

        ## Generate M2
        SRP_M2 = hashlib.sha1(SRP_A + SRP_M1 + SRP_SKhash).digest()

        ## Generate the CRC, (at the moment the CRC is not important)
        SRP_CRC = chr(0)*20

        print "*** Server Side Numbers ***"
        print "b = %s" % SRP_b.encode('hex')
        print "g = %x" % SRP_g
        print "n = %s" % SRP_n.encode('hex')
        print "k = %x" % SRP_k
        print "salt = %s" % SRP_salt.encode('hex')
        print
        print "*** Client Side Numbers ***"
        print "A = %s" % SRP_A.encode('hex')
        print "x = %s" % SRP_x.encode('hex')
        print "v = %x" % SRP_v
        print "u = %s" % SRP_u.encode('hex')
        print "S = %x" % SRP_S
        print "SK = %s" % SRP_SKhash.encode('hex')
        print
        print "*** Both Sides Numbers ***"
        print "Nhash = %s" % SRP_nhash.encode('hex')
        print "Ghash = %s" % SRP_ghash.encode('hex')
        print "Uhash = %s" % SRP_userhash.encode('hex')
        print "NGhash = %s" % SRP_nghash.encode('hex')
        print "M1 = %s" % SRP_M1.encode('hex')
        print "M2 = %s" % SRP_M2.encode('hex')
        print "CRC = %s" % SRP_CRC.encode('hex')
        print

        self.SRP_A = SRP_A
        self.SRP_M1 = SRP_M1
        self.SRP_M2 = SRP_M2
        self.SRP_CRC = SRP_CRC
        self.SRP_SK = SRP_SKhash

        self.CS_AUTH_LOGON_PROOF()      # Send the following packet

    def CS_AUTH_LOGON_PROOF(self):
        # Send AUTH_LOGON_PROOF
        data = struct.pack(
            ST_AUTH_LOGON_PROOF[0],          # Structure
            OP_AUTH_LOGON_PROOF,             # OpCode
            self.SRP_A,                      # A SRP value
            self.SRP_M1,                     # M1 SRP value
            self.SRP_CRC,                    # CRC value
        )

        self.buffer += data                   # Put the packet in the queue

    def SS_AUTH_LOGON_PROOF(self, data):
        #print "Auth Logon proof"
        #error = ord(data[1])
        #if error != 0:                              # Stop the program if an error occur
        #    print ER_AUTH_LOGON_PROOF[error]        # Print error message
        #    self.close()
        #    sys.exit()                              # Exit the program

        #struct_data = struct.unpack(ST_AUTH_LOGON_PROOF[1], data)   # Unpack the datas
        print "Logon Proof !"
        print self.SRP_M2.encode('hex')

        # Check if both M2 are the same
        #if self.SRP_M2 != struct_data[2]:                           # Check if server side M2 is the same as client side
        #    print "M2 differs, authentification failed !"
        #    sys.exit()

        self.CS_REALM_LIST()

    def CS_REALM_LIST(self):
        data = struct.pack(
            ST_REALM_LIST[0],          # Structure
            OP_REALM_LIST,             # OpCode
            0,                         # Key 
        )

        self.buffer += data

    def SS_REALM_LIST(self, data):
        #print "Realm list"
        self.realms = {}

        ## Get the header of this packet to know the size and the number of realms
        size = struct.calcsize(ST_REALM_LIST[1])                        # Get the size of the structure
        realm_header = struct.unpack(ST_REALM_LIST[1], data[:size])     # Unpack the header
        data = data[size:]                                              # Just use the following for after

        for i in range(realm_header[3]):
            size = struct.calcsize(ST_REALM_LIST[2])                    # Get the size of the structure
            realm_part1 = struct.unpack(ST_REALM_LIST[2], data[:size])  # Unpack the first fix size
            data = data[size:]                                          # Just use the following for after
            
            realm_name = ReadString(data)                               # Read until 0x00 is reached
            data = data[len(realm_name)+1:]                             # +1 for the leading 0x00
            
            realm_address = ReadString(data)                            # Same
            data = data[len(realm_address)+1:]                          # 

            size = struct.calcsize(ST_REALM_LIST[3])                    # Get the size of the structure
            realm_part2 = struct.unpack(ST_REALM_LIST[3], data[:size])  # unpack
            data = data[size:]                                          # Just use the following for after

            self.realms[realm_name] = {                                 # Add the realm with key realm_name
                'icon' : realm_part1[0],
                'locked' : realm_part1[1],
                'color' : realm_part1[2],
                'address' : realm_address,
                'population' : realm_part2[0],
                'nbchars' : realm_part2[1],
                'timezone' : realm_part2[2],
            }

        print self.realms
        self.close()

    def SS_UNKNOWN(self, data):
        print "Unknown packet 0x%s" % (data[0].encode("hex"))  

    def handle_connect(self):
        #print "Connection successfull"
        self.CS_AUTH_LOGON_CHALLENGE()

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        s = self.recv(4096)
        print "%d bytes read" % (len(s))
        print StrToProperHex(s)
        print
        self.packethandler.get(ord(s[0]), self.SS_UNKNOWN)(s)

    def handle_write(self):
        if self.buffer:
            sent = self.send(self.buffer)
            print "%d bytes written" % (sent)
            print StrToProperHex(self.buffer[:sent])
            print
            self.buffer = self.buffer[sent:]

    def handle_close(self):
        print "Connection closed."
        self.close()
