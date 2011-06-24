from construct import *

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

def process(data, env):
    # Modify the realm
    realmsList = ST_REALM_LIST_S_FULL.parse(data).Realm
    for r in realmsList:
        r.address = '127.0.0.1:8085'
        r.name += ' - PROXY'

    c = Container(
        unk1 = 0,
        nb_realms = len(realmsList),
        Realm = realmsList,
        unk2 = 0x10,
        unk3 = 0
    )
    pkt_p = ST_REALM_LIST_S_PAYLOAD.build(c)
    c = Container(
        opcode = 0x10,
        size = len(pkt_p)
    )
    pkt_h = ST_REALM_LIST_S_HEADER.build(c)

    return pkt_h + pkt_p
