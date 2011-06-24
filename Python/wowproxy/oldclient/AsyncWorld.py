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
        self.packet = ""
        self.length = -1
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
            0x0266 : self.SS_SET_FLAT_SPELL_MODIFIER,
            0x0267 : self.SS_SET_PCT_SPELL_MODIFIER,
            0x0329 : self.SS_SET_DUNGEON_DIFFICULTY,
            0x0096 : self.SS_MESSAGE_CHAT,
            0x02c2 : self.SS_INIT_WORLD_STATES,
            0x0051 : self.SS_REPONSE_PLAYER_NAME,
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
        self.serverseed = struct.unpack(ST_AUTH_CHALLENGE[0], data)[0]  # Get the server seed value
        print "Server Seed = %x" % self.serverseed                      # Output
        
        self.CS_AUTH_SESSION()                                          # Called to create response packet

    def CS_AUTH_SESSION(self):
        clientseed = random.getrandbits(32)                     # Create a client seed value
        #clientseed = int('884B31EB', 16)                       # Short circuit random value

        s = struct.pack('<%dsIII40s' % (len(self.username)),    # Create a struct for the string to hash to have correct types
            self.username,
            0,
            clientseed,
            self.serverseed,
            self.sessionkey
        )

        auth_digest = hashlib.sha1(s).digest()                  # Generate the authentification digest
        print
        print "Auth Digest = %s" % auth_digest.encode("hex")
        
        data = struct.pack(                                     # Create Auth session packet
            ST_AUTH_SESSION[0] % len(self.username),
            OP_AUTH_SESSION,
            0,
            9947,
            0,
            self.username,
            clientseed,
            auth_digest,
            0
        )

        self.buffer += [data]   # Append this packet to the buffer

    def SS_AUTH_RESPONSE(self, data):
        struct_data = struct.unpack(ST_AUTH_REPONSE[0], data)     # Unpack the data
        if struct_data[0] != 12:                    # If it's different of 12 we have an error
            print "World authentification error"
            self.close()                            # Close the connection
            sys.exit()                              # Exit the program
        else:
            print "World authentification complete"
            print
            self.CS_CHAR_ENUM()                     # Call char enum function

    def CS_CHAR_ENUM(self):
        data = struct.pack(
            ST_CHAR_ENUM[0],
            OP_CHAR_ENUM,
        )

        self.buffer += [data]   # Append this packet to the buffer

    def SS_CHAR_ENUM(self, data):
        char_header = struct.unpack(ST_CHAR_ENUM[1], data[:struct.calcsize(ST_CHAR_ENUM[1])])
        print "Number of chars = %d" % (char_header[0])
        data = data[struct.calcsize(ST_CHAR_ENUM[1]):]
        
        for i in range(char_header[0]):
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

    def SS_SET_FLAT_SPELL_MODIFIER(self, data):
        pass

    def SS_SET_PCT_SPELL_MODIFIER(self, data):
        pass

    def SS_SET_DUNGEON_DIFFICULTY(self, data):
        pass

    def SS_MESSAGE_CHAT(self, data):
        # Message Type is 1 byte, msg_lang is 4 bytes
        msg_type, msg_lang = struct.unpack(ST_MESSAGE_CHAT[0], data[:struct.calcsize(ST_MESSAGE_CHAT[0])])    # Unpack datas
        data = data[struct.calcsize(ST_MESSAGE_CHAT[0]):]                                                    # Remove read data
        
        if msg_lang == 11:                      # 11 is when a NPC speak
            # This values are received only if npc speak
            msg_npc_guid, msg_unk, msg_npc_name_len, msg_npc_name = struct.unpack(ST_MESSAGE_CHAT[1], data[:struct.calcsize(ST_MESSAGE_CHAT[1])])
            data = data[struct.calcsize(ST_MESSAGE_CHAT[1]):]

        # Get message sender guid
        msg_source_guid, msg_unk = struct.unpack(ST_MESSAGE_CHAT[2], data[:struct.calcsize(ST_MESSAGE_CHAT[2])])
        data = data[struct.calcsize(ST_MESSAGE_CHAT[2]):]

        if msg_type == 14:                      # 14 is a channel message
            # The channel name is sent only if the message is a channel message
            msg_channel = ReadString(data)      # String with no size precised os read until 0x00 is reached
            data = data[len(msg_channel)+1:]

        # Get message destination guid and message length
        msg_target_guid, msg_len = struct.unpack(ST_MESSAGE_CHAT[3], data[:struct.calcsize(ST_MESSAGE_CHAT[3])])
        data = data[struct.calcsize(ST_MESSAGE_CHAT[3]):]

        # Get the text from the remaining datas with length got from the previous bytes
        msg_text = data[:msg_len]
        data = data[msg_len:]

        self.CS_QUERY_PLAYER_NAME(msg_source_guid)

        print "Message from %d to %d: %s" % (msg_source_guid, msg_target_guid, msg_text)

    def CS_MESSAGE_CHAT(self, msg_type, msg_destination, msg_text, msg_lang):
        if msg_text:
            data = struct.pack(
                ST_MESSAGE_CHAT[4],
                OP_MESSAGE_CHAT,
                msg_type,
                msg_lang,
            )
            if msg_type in [6, 14]:       # Whisper or Channel message
                data += struct.pack(
                    ST_MESSAGE_CHAT[5] % (len(msg_destination), len(msg_text)),
                    msg_destination,
                    msg_text,
                )
            else:
                data += msg_text+chr(0)

            self.buffer += [data]
                

    def CS_JOIN_CHANNEL(self, channel, password=''):
        data = struct.pack(
            ST_JOIN_CHANNEL[0] % (len(channel)),     # Data structure
            OP_JOIN_CHANNEL,
            0,
            0,
            0,
            channel,                # Channel string
            )
        
        if password:                # Password string with 0x00 ending character only if a password 
            data += struct.pack(
                ST_JOIN_CHANNEL[1] % (len(password)),
                password,           # Channel password
            )

        self.buffer += [data]

    def SS_INIT_WORLD_STATES(self, data):
        # Fully connected to the world
        self.CS_JOIN_CHANNEL('world')
        self.CS_MESSAGE_CHAT(14, 'world', 'Hello World !', 0)                       # Message on channel world
        #self.CS_MESSAGE_CHAT(0, '', '.announce Petit test de broadcast ...', 0)    # Say message

    def CS_QUERY_PLAYER_NAME(self, guid):        
        data = struct.pack(             
            ST_QUERY_PLAYER_NAME[0],
            OP_QUERY_PLAYER_NAME,
            guid,                       # Only need to send the guid
        )

        self.buffer += [data]

    def SS_REPONSE_PLAYER_NAME(self, data):
        guid = struct.unpack(ST_RESPONSE_PLAYER_NAME[0], data[:struct.calcsize(ST_RESPONSE_PLAYER_NAME[0])])[0]
        data = data[struct.calcsize(ST_RESPONSE_PLAYER_NAME[0]):]

        name = ReadString(data)

        print "Player name for id %d is %s" % (guid, name)
        
    def SS_UNKNOWN(self, data):
        print "Unknown OpCode 0x%x" % (self.opcode)

    def OnSent(self, OpCode):
        if OpCode == OP_AUTH_SESSION:       # After this packet has been send we enable the encryption
            self.encrypt = True

    def handle_connect(self):
        #print "Connection successfull"
        pass

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):
        if not self.packet or len(self.packet[2:]) < self.length:       # If packet buffer is empty or the length of the buffer is smaller than expected packet
            self.packet += self.recv(5120)                              # Receive a packet up to 5k (maybe need to be ajusted)
        if self.length == -1:                                           # If no current packet length
            if self.encrypt:                                            # If the encryption is on
                self.header = self.DecryptPacket(self.packet[:4])       # Decrypt the header
            else:
                self.header = self.packet[:4]                           # Just return the 4 bytes
                
            self.length = struct.unpack('>H', self.header[:2])[0]       # Get the packet length without himself
            self.opcode = struct.unpack('<H', self.header[2:])[0]       # Get the opcode of the packet
        if len(self.packet[2:]) >= self.length:
            # Process the call of function and trunk self.packet
            print "[OpCode = %d] %d bytes read" % (self.opcode, self.length)                    # Output informations
            print StrToProperHex(self.packet[:self.length+2])                                   # Print Hex dump
            self.packethandler.get(self.opcode, self.SS_UNKNOWN)(self.packet[4:self.length+2])  # Call the function related to the opcode
            self.packet = self.packet[self.length+2:]                                           # Remove this packet from the buffer the +2 is for the opcode
            self.length = -1                                                                    # Set as no more known packet
            print

    def writable(self):                     # Called if the socket is writable
        return len(self.buffer) > 0         # Return if we have to write something or not
        
    def handle_write(self):
        if len(self.buffer) > 0:
            packetlength = len(self.buffer[0])
            packet = struct.pack('>H%ds' % packetlength,         # Append at the begginning the size of the packet
                                 packetlength,                   # 
                                 self.buffer[0])                 #
            header = struct.unpack(ST_HEADER[0], packet[:4])     # Get the header
            if self.encrypt:                                     # Encrypt the packet if needed
                encrypted = self.EncryptPacket(packet)
                sent = self.send(encrypted)                      # Send it crypted
            else:
                sent = self.send(packet)                         # Send it uncrypted
            print "%d bytes written [Encryption=%s]" % (sent, self.encrypt)     # Output informations
            print StrToProperHex(packet)                                        # Print hex dump
            print
            del self.buffer[0]          # Delete this packet from the packet buffer list
            self.OnSent(header[1])      # Call this function to setup something if a packet is sent

    def handle_close(self):
        print "Connection closed."
        self.close()
