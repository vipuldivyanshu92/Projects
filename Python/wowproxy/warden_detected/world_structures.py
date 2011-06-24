from construct import *

CLIENT_HEADER_STRUCT = Struct('CLIENT_HEADER_STRUCT',
    UBInt16('size'),
    ULInt32('opcode')
)

ST_AUTH_SESSION_C = Struct('AUTH_SESSION_C',
    ULInt32('build'),
    ULInt32('unk2'),
    CString('I'),
    ULInt32('unk3'),
    ULInt32('client_seed'),
    String('digest', 20),
    
)
