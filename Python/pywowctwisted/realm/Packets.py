#!/usr/bin/env python

from construct import *

AUTH_LOGON_CHALLENGE_S = Struct('AUTH_LOGON_PROOF_S',
    UBInt8('opcode'),
    UBInt8('error'),
    UBInt8('unk1'),
    String('B', 32),
    PascalString('g', length_field = UBInt8('length')),
    PascalString('N', length_field = UBInt8('length')),
    String('s', 32),
    String('unk2', 16)
)

AUTH_LOGON_CHALLENGE_C = Struct('AUTH_LOGON_PROOF_C',
    ULInt8('opcode'),
    ULInt8('error'),
    ULInt16('size'),
    String('gamename', 4, padchar = '\x00'),
    Array(3, UBInt8('version')),
    ULInt16('build'),
    String('platform', 4, padchar = '\x00'),
    String('os', 4, padchar = '\x00'),
    String('country', 4, padchar = '\x00'),
    ULInt32('timezone_bias'),
    Array(4, UBInt8('ip')),
    PascalString('I', length_field = UBInt8('length'))
)