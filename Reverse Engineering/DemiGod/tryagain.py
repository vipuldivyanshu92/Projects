from socket import *
from time import *
from datetime import *
import random

cyphers = {
    "x" : "0018",
}

### Server ###
Host = '209.124.63.232'
Port = 443

ts = int(mktime(datetime.now().timetuple()))    # timestamp

s = socket(AF_INET, SOCK_STREAM)

pkt = ""

### HandShake protocol ###
pkt += "0301"   # TLS 1.0
pkt += "%x" % ts
pkt += "%028x" % (random.getrandbits(224))
pkt += "00"     # Session Id length
pkt += "%04x" % (len(cyphers) * 2)  # Cypher Suites Length
for i in cyphers.values():          # Append cyphers
    pkt += i
pkt += "01"     # compression method Length
pkt += "00"     # compression method
pkt += "0033"   # Extension length
pkt += "0000001d001b0000187365637572652e696d70756c736564726976656e2e636f6d000a00080006001700180019000b00020100" # Extension

pkt = "%06x%s" % (len(pkt)/2, pkt)    # Add handshake length
pkt = "01" + pkt                    # Client Hello

### Packet Wrapper ###
pkt = "%04x%s" % (len(pkt)/2, pkt)
pkt = "160301" + pkt

s.connect((Host, Port))

s.send(pkt.decode("hex"))

print s.recv(4096).encode("hex")
