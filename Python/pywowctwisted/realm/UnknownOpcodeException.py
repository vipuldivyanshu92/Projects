#!/usr/bin/env python

class UnknownOpcodeException(Exception):
    def __init__(self, opcode):
        self.opcode = opcode
        
    def __str__(self):
        return repr(self.opcode)