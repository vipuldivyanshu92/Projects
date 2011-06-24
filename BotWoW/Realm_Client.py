# Import required librairies
import struct
import socket
import sys

import hashlib
import random
from SharedFunc import *

from OpCodes import *
from Structures import *
from Errors import *

import ConfigReader

def PrintRealms(d):
    print 'Aivalable Realms:'
    for r in d.keys():
        print '"%s" on %s' % (r, d[r]['address'])
        print ' chars : %d, population : %.6f, timezone : %d' %(d[r]['nbchars'], d[r]['population'], d[r]['timezone'])

# Beginning of the main loop
Config = ConfigReader.ReadConf('bot.conf')      # Get the configuration
#print Config                                   # Debug

# Create the socket and establish the connexion
RealmSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP Stream socket
RealmSock.connect((Config.get('realmadress', ''), 3724))        # Connect to the server

# Create the firt identification packet AUTH_LOGON_CHALLENGE
ulen = len(Config.get('username', ''))
data = struct.pack(
    ST_AUTH_LOGON_CHALLENGE[0]+"%ds" % (ulen),          # Modify the structure with respect to the username
    OP_AUTH_LOGON_CHALLENGE,                            # OpCode
    0x07,                                               # Error Code
    struct.calcsize(ST_AUTH_LOGON_CHALLENGE[0])-4+ulen, # Packet length
    "WoW",                                              # Game ID
    0x02,                                               # Version[1]
    0x03,                                               # Version[2]
    0x03,                                               # Version[3]
    7799,                                               # Build                 Note : String must be reverse cause of less endian in blizz packets
    "68x",                                              # Platform
    "niW",                                              # Operating System
    "RFrf",                                             # Language
    0x3c,                                               # Timezone
    127,                                                # IP[1]
    0,                                                  # IP[2]
    0,                                                  # IP[3]
    1,                                                  # IP[4]
    ulen,                                               # Account Name length
    Config.get('username', '').upper(),                 # Account Name
    )
    
RealmSock.send(data)                    # Send Data
#print data                             # Debug
data = RealmSock.recv(1024)             # Receive Data
#print data                             # Debug

## Handle error code in the received packet
error = ord(data[2])                        # Get the error Code
if error != 0:                              # Stop the program if an error occur
    print ER_AUTH_LOGON_CHALLENGE[error]    # Print error message
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
SRP_a = random.getrandbits(152)                                 # Get a random value of 19 bytes
#print "%x" % SRP_a
SRP_A = IntToStr(modexp(SRP_g, SRP_a, StrToInt(SRP_n[::-1])))[::-1]             # Here n is reversed

## Generate SRP_x
SRP_authstr = '%s:%s' % (Config.get('username', ''), Config.get('password', ''))    # Concatenate USER:PASS
SRP_userhash = hashlib.sha1(SRP_authstr.upper()).digest()                           # Get the SHA hash
SRP_x = hashlib.sha1(SRP_salt+SRP_userhash).digest()[::-1]                          # Get SHA of salted user hash

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
SRP_userhash = hashlib.sha1(Config.get('username', '').upper()).digest()

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

# Send AUTH_LOGON_PROOF
data = struct.pack(
    ST_AUTH_LOGON_PROOF[0],          # Structure
    OP_AUTH_LOGON_PROOF,             # OpCode
    SRP_A,                           # A SRP value
    SRP_M1,                          # M1 SRP value
    SRP_CRC,                         # CRC value
    )

RealmSock.send(data)                    # Send Data

# Receive AUTH_LOGON_PROOF
data = RealmSock.recv(1024)

error = ord(data[1])
if error != 0:                              # Stop the program if an error occur
    print ER_AUTH_LOGON_PROOF[error]        # Print error message
    sys.exit()                              # Exit the program

struct_data = struct.unpack(ST_AUTH_LOGON_PROOF[1], data)

# Check if both M2 are the same
if SRP_M2 != struct_data[2]:
    print "M2 differs, authentification failed !"
    sys.exit()

# Send REALM_LIST
data = struct.pack(
    ST_REALM_LIST[0],          # Structure
    OP_REALM_LIST,             # OpCode
    0,                         # Key 
    )

RealmSock.send(data)                    # Send Data

# Receive REALM_LIST
## Realms is a dictionnary with all realms
realms = {}
data = RealmSock.recv(1024)

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

    realms[realm_name] = {                                      # Add the realm with key realm_name
        'icon' : realm_part1[0],
        'locked' : realm_part1[1],
        'color' : realm_part1[2],
        'address' : realm_address,
        'population' : realm_part2[0],
        'nbchars' : realm_part2[1],
        'timezone' : realm_part2[2],
        }

#print data.encode('hex')           # Print remaining data 

print
PrintRealms(realms)                 # Print the realms

RealmSock.close()                   # Close the connexion, we finish with the realm
