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

from construct import *
from xml.dom import minidom
from exttypes import *

class dispatcher:    
    def __init__(self, XMLfiles):
        self.interfaces = {}

        for f in XMLfiles:
            xmldoc = minidom.parse(f)

            #Retreive the interface name, else raise Exception
            xml_interface = xmldoc.getElementsByTagName('interface')
            if xml_interface and xml_interface[0].attributes.has_key('name'):
                interface = xml_interface[0].attributes['name'].value
            else:
                raise Exception, 'XMLError, no interface specified in %s.' % (f)

            #Create an entry in the dictionnary for this interface
            if self.interfaces.has_key(interface):
                raise Exception, 'Interface redifinition, two XML files have the same interface'

            self.interfaces[interface] = {}

            for packet in xmldoc.getElementsByTagName('packet'):
                if not (packet.attributes.has_key('opcode') and packet.attributes.has_key('name') and packet.attributes['opcode'].value.isdigit()):
                    raise Exception, 'Attributes are missing or type is incorrect.'
                
                opcode = int(packet.attributes['opcode'].value)
                self.interfaces[interface][opcode] = {
                    'name' : str(packet.attributes['name'].value),
                    'struct' : Struct(str(packet.attributes['name'].value)),
                    'overwrite' : {}
                }

                #Set each field
                for field in packet.getElementsByTagName('field'):
                    if not (field.attributes.has_key('type') and field.attributes.has_key('name')):
                        raise Exception, 'Attributes are missing.'
                        
                    t = str(field.attributes['type'].value)
                    n = str(field.attributes['name'].value)
                    self.interfaces[interface][opcode]['struct'].subcons += tuple([globals()[t](n)])

                    if field.firstChild:
                        self.interfaces[interface][opcode]['overwrite'][n] = str(field.firstChild.data)

    def GetheaderStruct(self):
        return Struct('Header',
            UBInt32('pktSize'),
            string('Receiver'),
            UBInt32('unk1'),
            UBInt32('unk2'),
            string('Sender'),
            UBInt32('unk3'),
            UBInt32('unk4'),
            UBInt32('Opcode'),
        )

    def GetpacketStruct(self, interface, opcode):
        return self.interfaces[interface][opcode]['struct']

    def GetpacketOverwrite(self, interface, opcode):
        return self.interfaces[interface][opcode]['overwrite']

    def Getname(self, interface, opcode):
        return self.interfaces[interface][opcode]['name']

    def has_opcode(self, interface, opcode):
        return self.interfaces[interface].has_key(opcode)

