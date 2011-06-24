import AsyncRealm
import AsyncWorld
import ConfigReader
import asyncore
import socket

config = ConfigReader.ReadConf("bot.conf")

RealmSession = AsyncRealm.RealmHandler(
        config.get("realmaddress", "127.0.0.1"),
        config.get("username", ""),
        config.get("password", ""),
    )

asyncore.loop()

print RealmSession.realms
print

WorldSession = AsyncWorld.WorldHandler(
        RealmSession.realms.get(config.get("realmname", ""), "")["address"],
        #"127.0.0.1:8085",
        config.get("username", ""),
        RealmSession.SRP_SK,
        config.get("character", ""),
    )

asyncore.loop()
