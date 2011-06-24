from common import framework
from player import onAuthenticate, onGetStartupData, onCreateCharacter
import asyncore
import MySQLdb

class PlayerServer(framework.server):
    def __init__(self):
        framework.server.__init__(self, 7001, 20, framework.GlobalHandler, False)
        
        self.db = MySQLdb.connection(
            host   = "127.0.0.1",
            user   = "root",
            passwd = "",
            db     = "aoc",
        )
    
        self.packetMgr = {
            "PlayerAgent" : {
                0 : onAuthenticate.onAuthenticate,
                1 : onCreateCharacter.onCreateCharacter,
                6 : onGetStartupData.onGetStartupData,
            }
        }
        
        # Retrieving dimensions from database (prevent a request each time)
        self.dimensions = {}
        self.db.query("SELECT * FROM `dimensions`")
        r = self.db.store_result()
        for f in r.fetch_row(r.num_rows(), how=1):
            self.dimensions[int(f["dimension_id"])] = f
        
serv = PlayerServer()
asyncore.loop()