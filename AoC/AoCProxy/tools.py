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

import sys
from shared.packet import packet

compressed = False
if len(sys.argv) == 2 and sys.argv[1].upper() == 'TRUE':
    compressed = True
    
pkt = packet()
pkt.ReadFromBuffer(raw_input("packet hex dump : ").decode("hex"), compressed)

print
#print pkt.GetBuffer(False).encode("hex")
print pkt.opCode
print pkt.sender
print
print pkt.data.encode("hex")
