from Crypto.Cipher import ARC4
from construct import *
import hmac
import hashlib
import array

SK_s_h = 'C42DA0B5F98524964C503E921A48C70DF356E48B43F0AE857EE5E30B8DF3FB5B5A84EAC4237C003B'

# Server Encrypt
ServerEncryptKey = array.array('B', [0x22, 0xBE, 0xE5, 0xCF, 0xBB, 0x07, 0x64, 0xD9, 0x00, 0x45, 0x1B, 0xD0, 0x24, 0xB8, 0xD5, 0x45])
encryptHash = hmac.new(ServerEncryptKey.tostring(), SK_s_h.decode('hex')[::-1], hashlib.sha1).digest()
print encryptHash.encode('hex')

# Server Decrypt
ServerDecryptKey = array.array('B', [0xF4, 0x66, 0x31, 0x59, 0xFC, 0x83, 0x6E, 0x31, 0x31, 0x02, 0x51, 0xD5, 0x44, 0x31, 0x67, 0x98])
decryptHash = hmac.new(ServerDecryptKey.tostring(), SK_s_h.decode('hex')[::-1], hashlib.sha1).digest()
print decryptHash.encode('hex')

# Create encryption / decryption objects
clientDecrypt = ARC4.new(decryptHash)
serverEncrypt = ARC4.new(encryptHash)

# Do some synchronization
syncBuf = chr(0)*1024
serverEncrypt.encrypt(syncBuf)
clientDecrypt.decrypt(syncBuf)

# Some tests
#LENGTH: 13
#OPCODE: SMSG_AUTH_RESPONSE (0x01EE)
#Should get 97 1A 5A 91
# Opcode right / size wrong (why ?)
HEADER_STRUCT_SERVER = Struct('HEADER',
    UBInt16('size'),
    ULInt16('opcode'),
)

HEADER_STRUCT_CLIENT = Struct('HEADER',
    UBInt16('size'),
    ULInt16('opcode'),
)

# SMSG_AUTH_RESPONSE, should return 97 1A 5A 91
pkt = HEADER_STRUCT_SERVER.build(Container(size = 13, opcode = 0x01EE))
e_data = serverEncrypt.encrypt(pkt)
print e_data.encode('hex')

# SMSG_ADDON_INFO
pkt = HEADER_STRUCT_SERVER.build(Container(size = 182, opcode = 0x02EF))
e_data = serverEncrypt.encrypt(pkt)
print e_data.encode('hex')

# SMSG_TUTORIAL_FLAGS
pkt = HEADER_STRUCT_SERVER.build(Container(size = 34, opcode = 0x00FD))
e_data = serverEncrypt.encrypt(pkt)
print e_data.encode('hex')

# CMSG_CHAR_ENUM
data = '5A9BBD73B1D2'.decode('hex')
d_data = clientDecrypt.decrypt(data)
pkt = HEADER_STRUCT_CLIENT.parse(d_data)
print pkt
