#!/usr/bin/env python

# twisted import
from twisted.internet.protocol import Protocol

# packet import
from construct import *
from Packets import *
from Opcodes import *

# Exceptions
from UnknownOpcodeException import UnknownOpcodeException

class RealmProtocol(Protocol):
    """
        The realm server assure that every packet are sent one by one
    """
    
    def connectionMade(self):
        # Initialize the handle table
        self._handleTable = {
            AUTH_LOGON_CHALLENGE: self.handleLogonChallenge,
        }
        
        # Send the AUTH_LOGON_CHALLENGE to initiate the handshake
        pkt = AUTH_LOGON_CHALLENGE_C.build(Container(
            opcode = AUTH_LOGON_CHALLENGE,
            error = 0x08,
            size = 0x25,
            gamename = 'WoW',
            version = (3, 0, 9),
            build = 9551,
            platform = '68x',
            os = 'niW',
            country = 'RFrf', 
            timezone_bias = 0,
            ip = (127, 0, 0, 1),
            I = 'EOWAMIR'
        ))
        self.transport.write(pkt)
    
    def dataReceived(self, data):
        """ Translates bytes into packets, and call packetReceived"""
        if (not data):
            return
        
        opcode = ord(data[0])
        if (opcode in self._handleTable):
            self._handleTable[opcode](data)
        else:
            raise UnknownOpcodeException(opcode)
            
    def handleLogonChallenge(self, data):
        pkt = AUTH_LOGON_CHALLENGE_S.parse(data)
        print pkt