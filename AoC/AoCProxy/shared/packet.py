"""
Faolan Project, a free Age of Conan server emulator made for educational purpose
Copyright (C) 2008 Project Faolan team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

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
