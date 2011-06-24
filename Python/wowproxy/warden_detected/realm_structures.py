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

ST_AUTH_LOGON_CHALLENGE_S = Struct('AUTH_LOGON_CHALLENGE_S',
    ULInt8('opcode'),
    ULInt8('unk'),
    ULInt8('error'),
    String('SRP_B', 32),
    PascalString('SRP_g'),
    PascalString('SRP_N'),
    String('SRP_s', 32),
    String('CRC_salt', 16),
    ULInt8('security_flag')
)

ST_AUTH_LOGON_PROOF_C = Struct('AUTH_LOGON_PROOF_C',
    ULInt8('opcode'),
    String('SRP_A', 32),
    String('SRP_M1', 20),
    String('CRC', 20),
    ULInt16('unk')
)

ST_AUTH_LOGON_PROOF_S = Struct('AUTH_LOGON_PROOF_S',
    ULInt8('opcode'),
    ULInt8('error'),
    String('SRP_M2', 20),
    ULInt32('unk1'),
    ULInt32('unk2'),
    ULInt16('unk3')
)

ST_REALM = Struct('Realm',
        ULInt8('icon'),
        ULInt8('lock'),
        ULInt8('color'),
        CString('name'),
        CString('address'),
        LFloat32('population'),
        ULInt8('nb_characters'),
        ULInt8('timezone'),
        ULInt8('unk')
)

ST_REALM_LIST_S_HEADER = Struct('REALM_LIST_S_HEADER',
    ULInt8('opcode'),
    ULInt16('size')
)

ST_REALM_LIST_S_PAYLOAD = Struct('REALM_LIST_S',
    ULInt32('unk1'),
    ULInt16('nb_realms'),
    Array(lambda ctx: ctx['nb_realms'], ST_REALM),
    ULInt8('unk2'),
    ULInt8('unk3')
)

ST_REALM_LIST_S_FULL = Struct('REALM_LIST_S',
    Embed(ST_REALM_LIST_S_HEADER),
    Embed(ST_REALM_LIST_S_PAYLOAD)
)
