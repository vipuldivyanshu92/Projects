package auctionsystem.server;

import auctionsystem.libraries.Configuration;
import auctionsystem.shared.Bid;
import auctionsystem.libraries.Logger;
import java.rmi.RemoteException;
import java.util.Timer;
import java.util.TimerTask;

/**
 * Monitor the state of the auction and close them on expiration.
 * This class also rebuild the cache when necessary
 * @author Simon Jouet
 */
public class AuctionTimer {
    private int purge_delay;
    private Timer statusTimer;
    private Timer purgeTimer;
    private Logger logger;

    private class AuctionExpiresTask extends TimerTask {
        private int identifier;

        public AuctionExpiresTask(int identifier) {
            this.identifier = identifier;
        }

        public void run() {
            AuctionItemCollection auctions =
                    AuctionItemCollection.getInstance();

            // Retrieve the auction item
            AuctionItem item = auctions.get(identifier);

            synchronized (item) {
                // Close the auction
                item.closeAuction();

                // Get the highest bid
                Bid highestBid = item.getHighestBid();

                // No bid have been high enough
                if (highestBid == null ||
                        item.getMinValue() > highestBid.getValue())
                {
                    // Notify the creator of the auction
                    try {
                        item.getOwner().notification(
                            String.format("The minimum value for the item %s " +
                            "has not been reached",
                            item.getItemInfo().getName()));
                    } catch (RemoteException e) {
                        logger.warning("Unable to notify : %s", e.getMessage());
                    }

                    String message = String.format("No winner for the item %s "
                            + "the minimum value was £%.2f",
                            item.getItemInfo().getName(),
                            item.getMinValue());

                    for (Bid b : item.getBids()) {
                        try {
                            b.getBidder().notification(message);
                        } catch (RemoteException e) {
                            logger.warning("Unable to notify : %s",
                                e.getMessage());
                        }
                    }
                // Someone had a high enough bid
                } else {
                    // Send the message to the owner
                    try {
                        item.getOwner().notification(
                            String.format("Auction %d for the item %s has been"
                            + " won for £%.2f",
                            item.getItemInfo().getId(),
                            item.getItemInfo().getName(),
                            highestBid.getValue()));
                        
                        item.getOwner().notification(
                            String.format("The winner contact details are Name:"
                            + " %s Email: %s",
                            highestBid.getBidderName(), highestBid.getEmail()));
                    } catch (RemoteException e) {
                        logger.warning("Unable to notify : %s", e.getMessage());
                    }

                    // Send the message to the winner
                    try {
                        highestBid.getBidder().notification(
                                String.format("You won the item %s for £%.2f",
                                item.getItemInfo().getName(),
                                highestBid.getValue()));

                        highestBid.getBidder().processPayment(
                                item.getItemInfo(), highestBid);
                        
                    } catch (RemoteException e) {
                        logger.warning("Unable to notify : %s", e.getMessage());
                    }

                    // Send the message to the losers
                    String message = String.format(
                            "You lost the auction for the item %s the " +
                            "highest bid was £%.2f",
                            item.getItemInfo().getName(),
                            highestBid.getValue());

                    for (Bid b : item.getBids()) {
                        if (b == highestBid)
                            continue;

                        try {
                            b.getBidder().notification(message);
                        } catch (RemoteException e) {
                            logger.warning("Unable to notify : %s", e.getMessage());
                        }
                    }
                }


                logger.info("Auction %s has been closed",
                        item.getItemInfo().getId());
            }
        }
    }

    private class AuctionPurgeTask extends TimerTask {
        public void run() {
            // Concurrent Hashmap ensure that the iterator will not cause errors
            AuctionItemCollection coll = AuctionItemCollection.getInstance();
            for (AuctionItem item : coll.getValues()) {
                if (!item.isOpen())
                    coll.remove(item.getItemInfo().getId());
            }
            coll.rebuildCache();
        }
    }

    public AuctionTimer() {
        statusTimer = new Timer();
        purgeTimer = new Timer();
        logger = Logger.getInstance();
        purge_delay = Configuration.getInstance().getInt("purge-time", 5) *
                60 * 1000;

        logger.warning("Purge delay set at %d ms", purge_delay);

        // Run the purge timer
        purgeTimer.scheduleAtFixedRate(new AuctionPurgeTask(),
                purge_delay, purge_delay);
    }

    /**
     * Add an auctionItem to schedule for expiration
     * @param item AuctionItem to monitor
     */
    public void add(AuctionItem item) {
        logger.info("Scheduling AuctionItem %d for closing",
                item.getItemInfo().getId());

        statusTimer.schedule(new AuctionExpiresTask(item.getItemInfo().getId()),
            item.getItemInfo().getEndTime());
    }
}

