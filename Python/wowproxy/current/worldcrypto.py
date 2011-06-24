from Crypto.Cipher import ARC4
from construct import *
import hmac
import hashlib
import array

class WorldCrypto:
    encryptKey = array.array('B', [0x22, 0xBE, 0xE5, 0xCF, 0xBB, 0x07, 0x64, 0xD9, 0x00, 0x45, 0x1B, 0xD0, 0x24, 0xB8, 0xD5, 0x45])
    decryptKey = array.array('B', [0xF4, 0x66, 0x31, 0x59, 0xFC, 0x83, 0x6E, 0x31, 0x31, 0x02, 0x51, 0xD5, 0x44, 0x31, 0x67, 0x98])
    
    def __init__(self, SK, t='server'):
        self.encryptHash = hmac.new(self.encryptKey.tostring(), SK, hashlib.sha1).digest()
        self.decryptHash = hmac.new(self.decryptKey.tostring(), SK, hashlib.sha1).digest()

        # Create encryption / decryption objects
        if t == 'server':
            self.decrypt_obj = ARC4.new(self.decryptHash)
            self.encrypt_obj = ARC4.new(self.encryptHash)
        else:
            self.decrypt_obj = ARC4.new(self.encryptHash)
            self.encrypt_obj = ARC4.new(self.decryptHash)
           

        # Do some synchronization
        syncBuf = chr(0)*1024
        self.encrypt_obj.encrypt(syncBuf)
        self.decrypt_obj.decrypt(syncBuf)

    def encrypt(self, data):
        return self.encrypt_obj.encrypt(data)

    def decrypt(self, data):
        return self.decrypt_obj.decrypt(data)

