from commonenv import commonenv
from construct import *

ST_AUTH_LOGON_CHALLENGE_C = Struct('AUTH_LOGON_CHALLENGE_C',
    ULInt8('opcode'),
    ULInt8('error'),
    ULInt16('size'),
    String('gamename', 4, padchar = '\x00'),
    Array(3, ULInt8('version')),
    ULInt16('build'),
    String('platform', 4, padchar = '\x00'),
    String('os', 4, padchar = '\x00'),
    String('country', 4, padchar = '\x00'),
    ULInt32('timezone'),
    UBInt32('ip'),
    PascalString('I')
)

def process(data, env):
    pkt = ST_AUTH_LOGON_CHALLENGE_C.parse(data)
    commonenv[pkt.I] = env
    return data
