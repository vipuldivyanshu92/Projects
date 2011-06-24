package auctionsystem.shared;

import auctionsystem.exceptions.AuctionNotFoundException;
import auctionsystem.exceptions.BidInvalidException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.Collection;
import java.util.Date;

/**
 * Server Shared Interface for RMI
 * @author Adraen
 */
public interface IAuctionServer extends Remote {
    public int createAuction(String itemName, double minValue, Date endTime,
            IAuctionClient owner) throws RemoteException;

    public Collection<AuctionItemInfo> getAuctionItems()
            throws RemoteException;

    public void placeBid(int id, Bid bid)
            throws RemoteException, AuctionNotFoundException, BidInvalidException;
}
