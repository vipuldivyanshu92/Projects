# Import required librairies
import asyncore
import socket
import struct
import hashlib
import random
import sys
from SharedFunc import *
from World_OpCodes import *
from World_Structures import *
from World_Errors import *

class WorldHandler(asyncore.dispatcher):
    def __init__(self, worldaddress, username, sessionkey, character):  # Parameters for the connection
        self.username = username.upper()                                # Set the Username and password for next packets
        self.worldaddress = worldaddress.split(':')                     # World adress from the realms dictionnary
        self.sessionkey = sessionkey                                    # Session key from the realm
        self.character = character 
        self.data = ""
        self.send_i = 0
        self.send_j = 0                                                 # Init encrypt value buffer
        self.recv_j = 0                                                 # Init decrypt value buffer
        self.recv_i = 0
        self.encrypt = False                                            # Disable packet encryption
        self.characters = {}
        asyncore.dispatcher.__init__(self)                              # Overload the previous definition
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)          # Create the sock_stream socket
        self.connect((self.worldaddress[0], int(self.worldaddress[1]))) # Connect to the world_server
        self.buffer = []                                                # Init the data to send buffer

        self.packethandler = {                                          # Dictionnary with received opcode and function to call
            0x01ec : self.SS_AUTH_CHALLENGE,
            0x01ee : self.SS_AUTH_RESPONSE,
            0x003b : self.SS_CHAR_ENUM,
            0x0127 : self.SS_PROFICIENCY,
        }

    def EncryptPacket(self, data):
        l_data = list(data[:6])                                                     # Only the header is encrypted
        result = ""                                                                 # Init result variable
        for t in range(6):                                                          # Length of the header is 6
            self.send_i %= len(self.sessionkey)                                     #
            x = (ord(l_data[t]) ^ ord(self.sessionkey[self.send_i])) + self.send_j  # Calculate the xor value wrt the previous byte
            if x > 255:                                                             # Work all the time in a bytes
                x -= 256                                                            # Return the value as a overflown byte
            self.send_i += 1                                         
            self.send_j = x
            result += chr(x)
        return result+data[6:]                                                   # Return the packet with the uncrypt part too

    def DecryptPacket(self, data):
        l_data = list(data[:4])                                      # Only the header is encrypted
        result = ""
        for t in range(4):
            self.recv_i %= len(self.sessionkey)
            x = (ord(data[t]) - self.recv_j) ^ ord(self.sessionkey[self.recv_i])
            if x < 0:
                x += 256
            self.recv_i += 1
            self.recv_j = ord(data[t])
            result += chr(x)
        return result+data[4:]
        

    def SS_AUTH_CHALLENGE(self, data):
        struct_data = struct.unpack(ST_AUTH_CHALLENGE[0], data)     # Unpack the data
        self.serverseed = struct_data[2]                            # Get the server seed value
        print "Server Seed = %x" % self.serverseed                  # Output
        
        self.CS_AUTH_SESSION()                                      # Called to create response packet

    def CS_AUTH_SESSION(self):
        clientseed = random.getrandbits(32)                     # Create a client seed value
        #clientseed = int('A79087E3', 16)                       # Short circuit random value

        s = struct.pack('<11sIII40s',                           # Create a struct for the string to hash to have correct types
            self.username,
            0,
            clientseed,
            self.serverseed,
            self.sessionkey
        )

        auth_digest = hashlib.sha1(s).digest()                  # Generate the authentification digest
        print "Auth Digest = %s" % auth_digest.encode("hex")
        print

        data = struct.pack(                                     # Create Auth session packet
            ST_AUTH_SESSION[1] % len(self.username),
            OP_AUTH_SESSION,
            0,
            7799,
            0,
            self.username,
            clientseed,
            auth_digest,
            0
        )

        self.buffer += [data]   # Append this packet to the buffer

    def SS_AUTH_RESPONSE(self, data):
        struct_data = struct.unpack(ST_AUTH_REPONSE[0], data)     # Unpack the data
        if struct_data[2] != 12:
            print "World authentification error"
            self.close()
            sys.exit()                              # Exit the program
        else:
            print "World authentification complete"
            print
            self.CS_CHAR_ENUM()

    def CS_CHAR_ENUM(self):
        data = struct.pack(
            ST_CHAR_ENUM[0],
            OP_CHAR_ENUM,
        )

        self.buffer += [data]   # Append this packet to the buffer

    def SS_CHAR_ENUM(self, data):
        char_header = struct.unpack(ST_CHAR_ENUM[1], data[:struct.calcsize(ST_CHAR_ENUM[1])])
        print "Number of chars = %d" % (char_header[2])
        data = data[struct.calcsize(ST_CHAR_ENUM[1]):]
        
        for i in range(char_header[2]):
            char_guid = struct.unpack(ST_CHAR_ENUM[2], data[:struct.calcsize(ST_CHAR_ENUM[2])])
            data = data[struct.calcsize(ST_CHAR_ENUM[2]):]
            
            char_name = ReadString(data)
            data = data[len(char_name)+1:]
            
            char_struct = struct.unpack(ST_CHAR_ENUM[3], data[:struct.calcsize(ST_CHAR_ENUM[3])])
            data = data[struct.calcsize(ST_CHAR_ENUM[3]):]
            
            char_items = []
            for i in range(20):
                char_items += [struct.unpack(ST_CHAR_ENUM[4], data[:struct.calcsize(ST_CHAR_ENUM[4])])]
                data = data[struct.calcsize(ST_CHAR_ENUM[4]):]

            self.characters[char_name] = {
                "guid" : char_guid[0],
                "race" : char_struct[1],
                "class" : char_struct[2],
                "gender" : char_struct[3],
                "skin" : char_struct[4],
                "face" : char_struct[5],
                "hairstyle" : char_struct[6],
                "haircolour" : char_struct[7],
                "facialhair" : char_struct[8],
                "level" : char_struct[9],
                "zoneid" : char_struct[10],
                "mapid" : char_struct[11], 
                "posx" : char_struct[12],
                "posy" : char_struct[13],
                "posz" : char_struct[14],
                "guildid" : char_struct[15],
                "isrested" : char_struct[17],
                "petinfoid" : char_struct[18],
                "petlevel" : char_struct[19],
                "petfamilyid" : char_struct[20],
                "items" : char_items,
            }

        for c in self.characters.keys():
            print c
        print

        self.CS_PLAYER_LOGIN()

    def CS_PLAYER_LOGIN(self):
        data = struct.pack(
            ST_CHAR_LOGIN[0],
            OP_CHAR_LOGIN,
            self.characters.get(self.character, "")["guid"],
        )

        self.buffer += [data]

    def SS_PROFICIENCY(self, data):
        pass
        
    def SS_UNKNOWN(self, data):
        header = struct.unpack(ST_HEADER[0], data[:4])
        print "Unknown packet 0x%x" % (header[1])

    def OnSent(self, OpCode):
        if OpCode == OP_AUTH_SESSION:
            self.encrypt = True

    def handle_connect(self):
        #print "Connection successfull"
        pass

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        self.data += self.recv(5120)
        if len(self.data) > 4:
            print "%d bytes read [Encryption=%s]" % (len(self.data), self.encrypt)
            if self.encrypt == True:
                self.data = self.DecryptPacket(self.data)
            print StrToProperHex(self.data)
            print
            header = struct.unpack(ST_HEADER[0], self.data[:4])
            self.packethandler.get(header[1], self.SS_UNKNOWN)(self.data)
            self.data = ""

    def handle_write(self):
        if len(self.buffer) > 0:
            packetlength = len(self.buffer[0])
            packet = struct.pack('>H%ds' % packetlength,         # Append at the begginning the size of the packet
                                 packetlength,                   # 
                                 self.buffer[0])                 #
            header = struct.unpack(ST_HEADER[0], packet[:4])     # Get the header
            if self.encrypt ==  True:
                encrypted = self.EncryptPacket(packet)
                #print StrToProperHex(encrypted)
                sent = self.send(encrypted)
            else:
                sent = self.send(packet)
            print "%d bytes written [Encryption=%s]" % (sent, self.encrypt)
            print StrToProperHex(packet)
            print
            del self.buffer[0]
            self.OnSent(header[1])

    def handle_close(self):
        print "Connection closed."
        self.close()
