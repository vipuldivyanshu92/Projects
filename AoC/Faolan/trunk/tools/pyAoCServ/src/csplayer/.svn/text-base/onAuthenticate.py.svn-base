from .common import packet
from construct import *

class onAuthenticate:
    def __init__(self, handler, ipkt):
        print "here"
        # Parsing packet
        AuthenticateStruct = Struct("Authenticate",
            UBInt32("small_account_id"),
            UBInt32("cookie")
        )
        
        AuthenticateData = AuthenticateStruct.parse(ipkt.data)
        
        # Getting Infos from DataBase
        handler.server.db.query("SELECT * FROM `accounts` WHERE `account_id` = '%s'" % (AuthenticateData.small_account_id))
        r = handler.server.db.store_result()
        self.m_playerInfos = r.fetch_row(1, how=1)[0]
        
        if self.m_playerInfos["cookie"] == str(AuthenticateData.cookie):
            print "CSPlayer Authentification success for : %s" % (self.m_playerInfos["username"])
            handler.m_playerInfos = self.m_playerInfos
            handler.m_playerInfos["PlayerInstance"] = AuthenticateData.small_account_id
            
            opkt = packet.Packet(handler, 0)
            opkt.append_uint32(1)
            opkt.commit()
        else:
            print "Probably hacking attempt by : %s" % (self.m_playerInfos["username"])
            
            opkt = packet.Packet(handler, 0)
            opkt.append_uint32(0)
            opkt.commit()