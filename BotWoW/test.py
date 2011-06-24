import struct
import socket
import hashlib
import random

def modexp ( t, u, n ):
   #computes s = (t ^ u) mod n
   #args are base, exponent, modulus
   #(see Bruce Schneier's book, _Applied Cryptography_ p. 244)
   s = 1
   while u:
    	if u & 1:
    	   s = (s * t)%n
    	u >>= 1
    	t = (t * t)%n;
   return s

# Read a string from and return all char before 0x00
def ReadString(s):
   return s[:s.find(chr(0x00))]
      

# Configuration
username = "NECROALBERT"
password = "N3YL9RL5"

# Program
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("91.121.11.217", 3724))

data = struct.pack('<BBH4sBBBH4s4s4sIBBBBB11s',
                   0x00,            # OpCode
                   0x07,            # Error Code
                   0x0029,          # Packet Length
                   "WoW",           # Game ID
                   0x02,            # Version[1]
                   0x03,            # Version[2]
                   0x03,            # Version[3]
                   7799,            # Build
                   "68x",           # Platform
                   "niW",           # Operating System
                   "RFrf",          # Language
                   0x3c,            # Timezone
                   127,             # IP[1]
                   0,               # IP[2]
                   0,               # IP[3]
                   1,               # IP[4]
                   11,              # Account Name length
                   "NECROALBERT")   # Account Names

sock.send(data)

#print data.encode("hex")
#print
data = sock.recv(1024)
print data.encode("hex")
#print
data = struct.unpack('<BBB32sBBB32s32s16sx', data)
#data = struct.unpack('<BBB32sBBB32s32s16sx', '000000589a4c6065e985f7e408c91630699d5a266f8813dd1f51b7653261aec41a8c41010720b79b3e2a87823cab8f5ebfbf8eb10108535006298b5badbd5b53e1895e644b891baf31d06ef6416e649291a6ab433c3acabe8a6041a1d85315b4ff06c9acd18b096a36d0de22a97c7b8053c5d3d9c3d900'.decode("hex"))

b = data[3][::-1]
g = data[5]
n = data[7][::-1]
k = 3
salt = data[8][::-1]
unk3 = data[9][::-1]

print "*** Server side Numbers ***"
print "[B]%s" % (b.encode("hex"))
print "[G]%s" % (g)
print "[N]%s" % (n.encode("hex"))
print "[Salt]%s" % (salt.encode("hex"))
print "[Unk3]%s" % (unk3.encode("hex"))
print
print "*** Client side Numbers ***"

# Generate a
#a = random.getrandbits(152)
#a = int("573cce3af36cd63f127f3b971c040cdba151b6", 16)
print "[a]%x" % (a)

# Generate x
authstr = "%s:%s" % (username, password)
userhash = hashlib.sha1(authstr.upper()).digest()
x = hashlib.sha1(salt[::-1]+userhash).digest()[::-1]
print "[x]%s" % (x.encode("hex"))

# Generate v
tmp_x = int(x.encode("hex"), 16)
tmp_n = int(n.encode("hex"), 16)
v = str(modexp(g, tmp_x, tmp_n))
print "[v]%x" % (int(v))

# Generate A
A = str(modexp(g, a, tmp_n))
print "[A]%x" % (int(A))

# Generate u
tmp_A = "%x" % (int(A))
tmp_A = "%s%s" %("0"*(64-len(tmp_A)), tmp_A)
tmp_A = tmp_A.decode("hex")
u = hashlib.sha1(tmp_A[::-1]+b[::-1]).digest()[::-1]
print "[u]%s" % (u.encode("hex"))

# Generate S
tmp_b = int(b.encode("hex"), 16)
S = str(modexp(tmp_b - k*int(v), a + int(u.encode("hex"), 16) * int(x.encode("hex"), 16), tmp_n))
print "[S]%x" % (int(S))

# Generate Session Key
tmp_S = "%x" % (int(S))
tmp_S = tmp_S.decode("hex")[::-1]
S1 = ""
S2 = ""
for i in range(len(tmp_S)):
   if i % 2 == 0:
      S1 += tmp_S[i]
   else:
      S2 += tmp_S[i]
      
S1hash = hashlib.sha1(S1).digest()
S2hash = hashlib.sha1(S2).digest()

SShash = ""
for i in range(len(S1hash)):
   SShash += S1hash[i] + S2hash[i]
SShash = SShash[::-1]

print "[SK]%s" % (SShash.encode("hex"))
print
print "*** Common Numbers ***"

# Generate M1
nhash = hashlib.sha1(n[::-1]).digest()
ghash = hashlib.sha1(chr(g)).digest()
userhash = hashlib.sha1(username.upper()).digest()

print "[Nhash]%s" % (nhash.encode("hex"))
print "[Ghash]%s" % (ghash.encode("hex"))
print "[Uhash]%s" % (userhash.encode("hex"))

nghash = ""
for i in range(len(nhash)):
   nghash +=  chr(int(nhash[i].encode("hex"), 16) ^ int(ghash[i].encode("hex"), 16))

print "[NGhash]%s" % (nghash.encode("hex"))
temp = nghash
temp += userhash
temp += salt[::-1]
temp += tmp_A[::-1]
temp += str(b)[::-1]
temp += SShash[::-1]
M1 = hashlib.sha1(temp).digest()
print "[M1]%s" % (M1.encode("hex"))

# Generate M2
temp = tmp_A[::-1]
temp += M1
temp += SShash[::-1]
M2 = hashlib.sha1(temp).digest()
print "[M2]%s" % (M2.encode("hex"))

# Generate CRC
CRC = chr(0)*20
print "[CRC]%s" %(CRC.encode("hex"))

# Send Packet logon proof
data = struct.pack('<B32s20s20sxx',
                   0x01,
                   tmp_A[::-1],
                   M1,
                   CRC)

sock.send(data)

print data.encode('hex')
data = sock.recv(1024)
data = struct.unpack('<BB20sLxx', data)

if M2!=data[2]:
   print "M2 differs, authentification failed."

# Send packet to list realm
data = struct.pack('<BL',
                   0x10,
                   0)

sock.send(data)

data = sock.recv(1024)
print data.encode("hex")

realm_header = struct.unpack('<BHLB', data[0:8])
print realm_header
realm_info = struct.unpack('<BBBp', data[8:12])
Name = ReadString(data[12:])
print Name
addr_port = ReadString(data[12+len(Name)+1:])
print addr_port
realm_info += struct.unpack('<fBBBBx', data[12+len(Name)+1+len(addr_port)+1:])
print realm_info
