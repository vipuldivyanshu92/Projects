package auctionsystem.client;

import auctionsystem.shared.AuctionItemInfo;
import auctionsystem.shared.Bid;
import auctionsystem.shared.IAuctionClient;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;


/**
 * Provides the callback functions to the server
 * @author Simon Jouet
 */
public class AuctionClient extends UnicastRemoteObject
        implements IAuctionClient {

    public AuctionClient() throws RemoteException {
    }

    // Print a message on the standard output of the client
    public void notification(String message) throws RemoteException {
        System.out.println(message);
    }

    // Send a payment request
    public void processPayment(AuctionItemInfo info, Bid bid)
        throws RemoteException {

        System.out.printf("[NYI] Please process to payment for item %s and the"
                + " amount £%.2f\n", info.getName(), bid.getValue());
    }
}
