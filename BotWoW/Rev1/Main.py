import AsyncRealm
import ConfigReader
import asyncore
import socket

config = ConfigReader.ReadConf("bot.conf")

request = AsyncRealm.RealmHandler(
        config.get("realmaddress", "127.0.0.1"),
        config.get("username", ""),
        config.get("password", ""),
    )

asyncore.loop()

print request.realms

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the sock_stream socket
sock.connect(("91.121.11.217", 8085))                     # Connect to the world_server
data = sock.recv(1024)
print data.encode("hex")
