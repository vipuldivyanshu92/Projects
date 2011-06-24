#!/usr/bin/env python

import struct
import zlib

"""
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
    def ReadFromBuffer(self, buffer, compressed):
        if compressed:
            inflateobj = zlib.decompressobj()
            buffer = inflateobj.decompress(buffer[5:])
            self.header = buffer[:5]
        pointer = 0
        self.length, self.senderLength = struct.unpack('!IH', buffer[pointer:pointer+6])
        pointer += 6
        self.sender = struct.unpack('!%ds' % (self.senderLength), buffer[pointer:pointer+self.senderLength])[0]
        pointer += self.senderLength
        self.unk1, self.unk2, self.receiverLength = struct.unpack('!IIH', buffer[pointer:pointer+10])
        pointer += 10
        self.receiver = struct.unpack('!%ds' % (self.receiverLength), buffer[pointer:pointer+self.receiverLength])[0]
        pointer += self.receiverLength
        self.unk3, self.unk4, self.opCode = struct.unpack('!III', buffer[pointer:pointer+12])
        pointer += 12
        self.data = buffer[pointer:self.length+4]
        self.size = self.length + 4
        
    def GetBuffer(self, compressed):
        size = 2+len(self.sender)+4+4+2+len(self.receiver)+4+4+4+len(self.data)
        buffer = struct.pack('!IH%dsIIH%dsIII%ds' % (len(self.sender), len(self.receiver), len(self.data)), size, len(self.sender), self.sender, self.unk1, self.unk2, len(self.receiver), self.receiver, self.unk3, self.unk4, self.opCode, self.data)
        if compressed:
            buffer = self.header + zlib.compress(buffer)
        return buffer