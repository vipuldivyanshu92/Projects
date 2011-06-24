#!/usr/bin/env python

import struct

class pwstring:
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return struct.pack('!H%ds' % (len(self.string)),
            len(self.string),
            self.string
        )

"""
    >> Header structure
    uint32 : I : Packet length
    uint16 : H : String length
    string : %ds : Sender
    uint32 : unk1
    uint32 : unk2
    uint16 : Receiver length
    string : Receiver
    uint32 : unk3
    uint32 : unk4
    uint32 : Opcode
"""

class packet:
    def __init__(self, sender, receiver, opcode = 0x0000, endian = '!'):
        self.header = ''
        self.headersize = 4+2+len(sender)+4+4+2+len(receiver)+4+4+4
        self.data = ''
        self.sender = sender
        self.receiver = receiver
        self.opcode = opcode
        self.endian = endian
    
    def set(self, data):
        self.header = data[:self.headersize]
        self.data = data[self.headersize:]
        self.opcode = struct.unpack('!H', data[self.headersize-2:self.headersize])[0]
    
    def append(self, type, data):
        self.data += struct.pack(self.endian + type, data)
        
    def appendpwstr(self, s):
        s = str(pwstring(s))
        self.data += s
    
    def delete(self, type):
        self.data = self.data[:-struct.calcsize(type)]
        
    def size(self):
        return self.headersize + len(self.data)
    
    def get(self):
        # Generate the header
        self.header = struct.pack(self.endian + 'IH%dsIIH%dsIII' % (len(self.sender), len(self.receiver)),
            self.headersize-4+len(self.data),
            len(self.sender),
            self.sender,
            0x00000000,
            0x00000000,
            len(self.receiver),
            self.receiver,
            0x00000000,
            0x00000000,
            self.opcode
        )
        # Concatenate the header and the datas
        return self.header + self.data