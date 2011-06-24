
package auctionsystem.server;

import auctionsystem.exceptions.AuctionNotFoundException;
import auctionsystem.exceptions.BidInvalidException;
import auctionsystem.shared.AuctionItemInfo;
import auctionsystem.shared.Bid;
import auctionsystem.shared.IAuctionClient;
import auctionsystem.shared.IAuctionServer;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.Collection;
import java.util.Date;
import java.util.LinkedList;
import java.util.concurrent.ConcurrentHashMap;

/**
 *
 * @author Adraen
 */
public class AuctionServer extends UnicastRemoteObject implements IAuctionServer {

    private final ConcurrentHashMap<Integer, AuctionItem> auctions;
    private int auctionId;

    public AuctionServer() throws RemoteException {
        auctions = new ConcurrentHashMap<Integer, AuctionItem>();
    }

    public int createAuction(String itemName, double minValue, Date endTime,
            IAuctionClient owner) {

        int aid = (auctionId + 1) % Integer.MAX_VALUE;
        AuctionItem item = new AuctionItem(aid, itemName, minValue, endTime, owner);

        auctions.put(aid, item);

        return aid;
    }

    public Collection<AuctionItemInfo> getAuctionItems() {
        LinkedList<AuctionItemInfo> infos = new LinkedList<AuctionItemInfo>();
        
        for (AuctionItem item : auctions.values())
            infos.add(item.getItemInfo());
        
        return infos;
    }

    public void placeBid(int id, Bid bid)
            throws AuctionNotFoundException, BidInvalidException {
        AuctionItem item = auctions.get(id);

        if (item == null)
            throw new AuctionNotFoundException();

        if (!(bid.getValue() > item.getHighestBid().getValue()))
            throw new BidInvalidException("Amount is too low");

        item.addBid(bid);
    }
}
