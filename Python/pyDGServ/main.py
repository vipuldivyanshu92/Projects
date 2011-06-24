#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.internet import reactor
from OpenSSL import SSL
from lxml import etree

class QOTD(Protocol):    
    def dataReceived(self, data):
        # Just get the XML part, (need to be redone, maybe use WEB Protocol of twisted)
        spData = data.split("\r\n\r\n")
        xmlData = spData[-1]
        
        if (xmlData == ""):
            return
            
        rcvRoot = etree.XML(xmlData)
        print "Received : %s" % (rcvRoot.tag)
        
        pktRoot = None
        
        if (rcvRoot.tag == "CVPGetApplicationInfoRequest"):
            pktRoot = etree.Element("CVPGetApplicationInfoResponse")
            responseCode = etree.SubElement(pktRoot, "ResponseCode")
            responseCode.text = "0"
            responseMessage = etree.SubElement(pktRoot, "ResponseMessage")
            responseMessage.text = "Success"
            
        elif (rcvRoot.tag == "CVPLoginRequest"):
            # Creating the xml packet
            pktRoot = etree.Element("CVPLoginResponse")
            
            # Retrieving previous values
            passElement = rcvRoot.find("Password")
            loginElement = rcvRoot.find("LoginID")
            
            # If this packet have no credentials something is wrong
            if ((passElement is None ) or (loginElement is None)):
                self.transport.loseConnection()
            else:
                passElement.text = passElement.text.strip()
                loginElement.text = loginElement.text.strip()
                # If the credentials texts are empty something is wrong
                if ((passElement.text == "") or (loginElement.text == "")):
                    self.transport.loseConnection()
                else:
                    responseCode = etree.SubElement(pktRoot, "ResponseCode")
                    responseCode.text = "0"
                    responseMessage = etree.SubElement(pktRoot, "ResponseMessage")
                    responseMessage.text = "Success"
                    token = etree.SubElement(pktRoot, "Token")
                    token.text = "FGwgwUFlgN8BaKkBT23w9AmMa/D8bH9I95HuufI5AcB9Ph1Rxj8dCISPM/SAcijgDArCgUTseF1Tj2yIEbe1y4FR0VUGO/tVCWkJmCLfDCOgn3PbaPp4rvuAqZZ0Vjiako1W6LYXAlPnqiyJB1JUuwWRqGlzp2qQ0c+lT2D3mUUUiCIw+kBe2pCEcrxqpVkq0WFeL8W8jbxE1dXAUGYdaEpUHm/kf7gd/FvA0RIm1tc0gv6Zw5nOqbesJE4ijnvPJETTIZM6n6+tNNvItekUh9su58f/GkOWQ/JPvhck7Z+/uBLF6ssWDjLtnJTJdO9QIbPIx5oFKuerLbmwJPp8Q90t478yUwCqaWO+mkrJ4aREOqzOfSL30h/M+AhRhNmgEd00yUQ9JmZ7X1zS8EmupxVxfwSRZSUVDNI6uw+59sea+442Jf/jGPPT+XgurELiFq/ymjuDBIOZqkkKaejb4sB5vViGrLjrMMLIv8Xd10pgUOzhIQgR6mL0myIOA2Mh"
                    players = etree.SubElement(pktRoot, "Players")
                    player = etree.SubElement(players, "Player")
                    default = etree.SubElement(player, "Default")
                    default.text = "true"
                    playerId = etree.SubElement(player, "PlayerID")
                    playerId.text = "15769"
                    playerName = etree.SubElement(player, "PlayerName")
                    playerName.text = "Adraen"
                    titleId = etree.SubElement(player, "TitleID")
                    titleId.text = "444"
                    playerData = etree.SubElement(player, "PlayerData")
                    aiPlayer = etree.SubElement(player, "AIPlayer")
                    aiPlayer.text = "false"
                    mmGroup = etree.SubElement(player, "MMGroup")
                    mmGroup.text = "1"
                    earnedFavorPts = etree.SubElement(player, "EarnedFavorPts")
                    earnedFavorPts.text = "0"
                    spentFavorPts = etree.SubElement(player, "SpentFavorPts")
                    spentFavorPts.text = "0"
                    currentFavorPts = etree.SubElement(player, "CurrentFavorPts")
                    currentFavorPts.text = "0"
                    specialtyItems = etree.SubElement(player, "SpecialtyItems")
                    currentWinningStreak = etree.SubElement(player, "CurrentWinningStreak")
                    currentWinningStreak.text = "0"
                    currentLosingStreak = etree.SubElement(player, "CurrentLosingStreak")
                    currentLosingStreak.text = "0"
                    currentDropoutStreak = etree.SubElement(player, "CurrentDropoutStreak")
                    currentDropoutStreak.text = "0"
                    largestWinningStreak = etree.SubElement(player, "LargestWinningStreak")
                    largestWinningStreak.text = "0"
                    largestLosingStreak = etree.SubElement(player, "LargestLosingStreak")
                    largestLosingStreak.text = "0"
                    largestDropoutStreak = etree.SubElement(player, "LargestDropoutStreak")
                    largestDropoutStreak.text = "0"
                    totalWins = etree.SubElement(player, "TotalWins")
                    totalWins.text = "0"
                    totalLosses = etree.SubElement(player, "TotalLosses")
                    totalLosses.text = "0"
                    totalDropouts = etree.SubElement(player, "TotalDropouts")
                    totalDropouts.text = "0"
                    totalPlaytime = etree.SubElement(player, "TotalPlaytime")
                    totalPlaytime.text = "0"
                    
                    
        if (pktRoot is not None):
            xml = etree.tostring(pktRoot)
            print xml
            v = "HTTP/1.0 200 OK\r\nDate: Sat, 15 Jan 2000 14:37:12 GMT\r\nServer: Microsoft-IIS/2.0\r\nContent-Type: text/xml\r\nContent-Length: %d\r\n\r\n%s"
            self.transport.write(v % (len(xml), xml))
        else:
            print "Not Handled : %s" % (rcvRoot.tag)
            self.transport.lostConnection()

# Create the factory
factory = Factory()
factory.protocol = QOTD

# Create the SSL Context, with server.pem as certificate, and TLS type auth
context = DefaultOpenSSLContextFactory('server.pem', 'server.pem', SSL.TLSv1_METHOD)

# Run the server
reactor.listenSSL(443, factory, context)
reactor.run()
