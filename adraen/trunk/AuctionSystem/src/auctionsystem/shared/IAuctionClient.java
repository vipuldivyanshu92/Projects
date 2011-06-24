package auctionsystem.shared;

import java.rmi.Remote;
import java.rmi.RemoteException;


/**
 * Client Shared Interface for RMI
 * @author Simon Jouet
 */

public interface IAuctionClient extends Remote {
    public void notification(String message) throws RemoteException;

    public void processPayment(AuctionItemInfo info, Bid bid)
            throws RemoteException;
}
