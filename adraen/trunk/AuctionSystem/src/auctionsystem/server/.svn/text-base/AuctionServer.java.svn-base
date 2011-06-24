package auctionsystem.server;

import auctionsystem.exceptions.AuctionNotFoundException;
import auctionsystem.exceptions.BidInvalidException;
import auctionsystem.shared.AuctionItemInfo;
import auctionsystem.shared.Bid;
import auctionsystem.shared.IAuctionClient;
import auctionsystem.shared.IAuctionServer;
import auctionsystem.libraries.Logger;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.Collection;
import java.util.Date;

/**
 * Auction Server that provides function through RMI
 * @author Simon Jouet
 */
public class AuctionServer extends UnicastRemoteObject
        implements IAuctionServer {

    private Logger logger;
    private AuctionItemCollection auctions;
    private AuctionTimer cleaner;

    public AuctionServer() throws RemoteException {
        logger = Logger.getInstance();
        auctions = AuctionItemCollection.getInstance();
        cleaner = new AuctionTimer();
    }

    /**
     * Create a new auction with the specified informations
     * @param itemName Long name of the item
     * @param minValue minimum value of the item required
     * @param endTime End of the auction for the specified item
     * @param owner AuctionClient associated to this bid used for callback
     * @return the bid Identifier
     * @throws RemoteException on RMI error
     */
    public int createAuction(String itemName, double minValue, Date endTime,
            IAuctionClient owner) throws RemoteException {

        int auctionId = auctions.getUniqueId();
        AuctionItem item = new AuctionItem(auctionId, itemName, minValue, endTime, owner);

        // make sure that nothing happens to the item before it has been
        // added to the auction collection and to the cleaner
        synchronized (item) {
            auctions.add(auctionId, item);
            cleaner.add(item);
        }

        logger.info("Creating auction %d", auctionId);

        return auctionId;
    }

    /**
     * Get the list of the available auction items
     * @return a collection of AuctionItem
     * @throws RemoteException on RMI error
     */
    public Collection<AuctionItemInfo> getAuctionItems()
            throws RemoteException {
        
        logger.debug("Query Auction items");
        
        return auctions.getCachedAuctionItemInfo();
    }


    /**
     * Place a bid on the specified item identifier
     * @param id item identifier
     * @param bid Bid object to represent the bid
     * @throws AuctionNotFoundException when bid does not exists
     * @throws BidInvalidException when the bid is lower than the previous one
     * @throws RemoteException on RMI error
     */
    public void placeBid(int id, Bid bid)
            throws AuctionNotFoundException, BidInvalidException,
            RemoteException {

        logger.info("Placing a new bid for item %d", id);

        AuctionItem item = auctions.get(id);

        if (item == null) {
            logger.warning("Auction %d does not exists", id);
            throw new AuctionNotFoundException();
        }

        synchronized (item) {
            if (!item.isOpen()) {
                logger.warning("Attempt to place a bid on the closed item %d", id);
                throw new BidInvalidException("Auction is closed for this item");
            }

            if (item.getHighestBid() != null &&
                    bid.getValue() <= item.getHighestBid().getValue()) {
                logger.info("Bid too low on item %d", id);
                throw new BidInvalidException("Amount is too low");
            }

            item.addBid(bid);
        }
    }
}
