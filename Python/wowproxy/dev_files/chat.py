from construct import *

CHAT_MSG_ADDON                  = 0xFFFFFFFF,
CHAT_MSG_SYSTEM                 = 0x00,
CHAT_MSG_SAY                    = 0x01,
CHAT_MSG_PARTY                  = 0x02,
CHAT_MSG_RAID                   = 0x03,
CHAT_MSG_GUILD                  = 0x04,
CHAT_MSG_OFFICER                = 0x05,
CHAT_MSG_YELL                   = 0x06,
CHAT_MSG_WHISPER                = 0x07,
CHAT_MSG_WHISPER_INFORM         = 0x08,
CHAT_MSG_REPLY                  = 0x09,
CHAT_MSG_EMOTE                  = 0x0A,
CHAT_MSG_TEXT_EMOTE             = 0x0B,
CHAT_MSG_MONSTER_SAY            = 0x0C,
CHAT_MSG_MONSTER_PARTY          = 0x0D,
CHAT_MSG_MONSTER_YELL           = 0x0E,
CHAT_MSG_MONSTER_WHISPER        = 0x0F,
CHAT_MSG_MONSTER_EMOTE          = 0x10,
CHAT_MSG_CHANNEL                = 0x11,
CHAT_MSG_CHANNEL_JOIN           = 0x12,
CHAT_MSG_CHANNEL_LEAVE          = 0x13,
CHAT_MSG_CHANNEL_LIST           = 0x14,
CHAT_MSG_CHANNEL_NOTICE         = 0x15,
CHAT_MSG_CHANNEL_NOTICE_USER    = 0x16,
CHAT_MSG_AFK                    = 0x17,
CHAT_MSG_DND                    = 0x18,
CHAT_MSG_IGNORED                = 0x19,
CHAT_MSG_SKILL                  = 0x1A,
CHAT_MSG_LOOT                   = 0x1B,
CHAT_MSG_MONEY                  = 0x1C,
CHAT_MSG_OPENING                = 0x1D,
CHAT_MSG_TRADESKILLS            = 0x1E,
CHAT_MSG_PET_INFO               = 0x1F,
CHAT_MSG_COMBAT_MISC_INFO       = 0x20,
CHAT_MSG_COMBAT_XP_GAIN         = 0x21,
CHAT_MSG_COMBAT_HONOR_GAIN      = 0x22,
CHAT_MSG_COMBAT_FACTION_CHANGE  = 0x23,
CHAT_MSG_BG_SYSTEM_NEUTRAL      = 0x24,
CHAT_MSG_BG_SYSTEM_ALLIANCE     = 0x25,
CHAT_MSG_BG_SYSTEM_HORDE        = 0x26,
CHAT_MSG_RAID_LEADER            = 0x27,
CHAT_MSG_RAID_WARNING           = 0x28,
CHAT_MSG_RAID_BOSS_WHISPER      = 0x29,
CHAT_MSG_RAID_BOSS_EMOTE        = 0x2A,
CHAT_MSG_FILTERED               = 0x2B,
CHAT_MSG_BATTLEGROUND           = 0x2C,
CHAT_MSG_BATTLEGROUND_LEADER    = 0x2D,
CHAT_MSG_RESTRICTED             = 0x2E,
CHAT_MSG_BN                     = 0x2F,
CHAT_MSG_ACHIEVEMENT            = 0x30,
CHAT_MSG_GUILD_ACHIEVEMENT      = 0x31

#   SAY
#   YELL
#   EMOTE
#   CHANNEL
#   WHISPER
#   GUILD
#   REPLY
#   GUILD_ACHIEVEMENT
CHAT_MSG_STRUCT = Struct('CHAT_MSG_WHISPER',
    ULInt8('type'),
    ULInt32('lang'),
    ULInt64('target_guid'),
    ULInt32('unk'),
    # the channel is present only on CHAT_MSG_CHANNEL(0x11)
    If(lambda ctx: ctx['type'] == 0x11,
        CString('channel'),
    ),
    # the name of the creature is present on CHAT_MSG_MONSTER_SAY
    If(lambda ctx: ctx['type'] == 0x0c,
        PascalString('name', length_field=ULInt32('length')),
    ),
    ULInt64('target_guid_2'),
    PascalString('message', length_field=ULInt32('length')),
    # the achievementID is present only on CHAT_MSG_ACHIEVEMENT(0x31)
    If(lambda ctx: ctx['type'] == 0x31,
        Embed(Struct('achievement',
            Padding(1),
            ULInt32('achivementId')
        ))
    ),
    # The chatTag is not present on CHAT_MSG_GUILD_ACHIEVEMENT(0x31)
    If(lambda ctx: ctx['type'] != 0x31,
        ULInt8('chatTag')
    ),
)


    

# CHAT_MSG_SAY
pkt = '01 00000000 3000000000000000 00000000300000000000000008000000 74 65 73 74 73 61 79 0004'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_CHANNEL
pkt = '11 00000000 7944000000000000 00000000 776f726c6400 7944000000000000 17000000 73616c75746174696f6e206120766f757320746f757300 00'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_WHISPER
pkt = '07000000007c42000000000000000000007c42000000000000080000006c6f6c696c6f6c0000'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_GUILD
pkt = '040000000058040000000000000000000058040000000000000f0000006e27696d706f7274652071756f690000'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_YELL
pkt = '060000000030000000000000000000000030000000000000000a0000007465737473686f75740004'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_REPLY
pkt = '090000000030000000000000000000000030000000000000000900000074657374776973700004'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_GUILD_ACHIEVEMENT
pkt = '31000000008609000000000000050000008609000000000000310000007c48706c617965723a244e7c685b244e5d7c682061206163636f6d706c69206c65206861757420666169742024612021000085000000'.replace(' ', '').decode('hex')
print CHAT_MSG_STRUCT.parse(pkt)

# CHAT_MSG_MONSTER_SAY
pkt = '0c 01000000 2227003c290030f1 00000000 10000000 50c3a96f6e206661696ec3a9616e7400 1343db0100008006 2a000000 41c3af65c2a021204f4b2c206a65207265746f75726e65206175207472617661696c2c20244ec2a02100 00'.replace(' ', '').decode('hex')
p = CHAT_MSG_STRUCT.parse(pkt)
print p
print p.name.decode('UTF-8')
print p.message.decode('UTF-8')

pkt = '0c01000000320800d70c0030f1000000000900000048616e61277a7561001343db01000080063100000048c3a274657a2d766f75732c20246e2e204d6f6e2064657374696e2065737420656e74726520766f73206d61696e732e0000'.replace(' ', '').decode('hex')
p = CHAT_MSG_STRUCT.parse(pkt)
print p
print p.name.decode('UTF-8')
print p.message.decode('UTF-8')
