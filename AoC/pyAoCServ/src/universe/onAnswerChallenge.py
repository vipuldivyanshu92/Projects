import random
import encryption
from .common import packet
from construct import *

class onAnswerChallenge:
    def __init__(self, handler, ipkt):       
        AnswerChallengeStruct = Struct("AnswerChallenge",
            UBInt32("unk1"),
            UBInt32("unk2"),
            UBInt16("unk3"),
            UBInt16("LoginDataSize"),
            MetaField("LoginData", lambda ctx: ctx["LoginDataSize"]),
        )
        
        tok = ipkt.data[2:].split('-')
        DecryptedData = encryption.Decrypt(tok[0], tok[1])
        loginData = AnswerChallengeStruct.parse(DecryptedData)
                
        (username, key, password) = loginData.LoginData.split('|')
        
        print "%s is trying to connect." % (username)
            
        handler.server.db.query("SELECT * FROM `accounts` WHERE `username` = '%s'" % (username))
        r = handler.server.db.store_result()
        handler.m_playerInfos = r.fetch_row(1, how=1)[0]
        
        if (str(key) == handler.server_hash) and (password == handler.m_playerInfos["password"]):
            print "Keys match authentification OK"
            # Sending Region Data (unknown datas)
            opkt = packet.Packet(handler, 5, "Universe")
            opkt.append("000000000000000200000000010101013f8000003f80000001010000000008".decode("hex"))
            opkt.commit()
            
            # Need to calculate a cookie for authentification
            cookie = random.getrandbits(32)
            
            # Update the Database
            handler.server.db.query("UPDATE `accounts` SET `cookie` = '%s', `last_connection` = NOW(), `last_ip` = '%s' WHERE `account_id` = '%s'" % (cookie, handler.client_addr[0], handler.m_playerInfos["account_id"]))
            handler.server.db.commit()
            
            # Sending AckAuthenticate
            opkt = packet.Packet(handler, 1, "Universe")
            opkt.append_uint32(1)
            opkt.append_uint64(long(handler.m_playerInfos["account_id"]))
            opkt.append_string("127.0.0.1:7001")
            opkt.append_uint32(cookie)
            opkt.append_uint32(0)
            opkt.commit()
            
            
        else:
            print "Authentification failed for user : %s" % (username)
            opkt = packet.Packet(handler, 1, "Universe")
            opkt.append_uint32(0xFFFFFFFF)
            opkt.append_uint32(0)
            opkt.append_uint32(0)
            opkt.append_uint32(0)
            opkt.append_uint32(0)
            opkt.append_uint16(1)
            opkt.commit()