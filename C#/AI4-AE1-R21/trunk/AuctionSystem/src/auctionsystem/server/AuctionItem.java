package auctionsystem.server;

import auctionsystem.shared.AuctionItemInfo;
import auctionsystem.shared.AuctionStatus;
import auctionsystem.shared.Bid;
import auctionsystem.shared.IAuctionClient;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;

/**
 *
 * @author Adraen
 */
public class AuctionItem {

    private AuctionItemInfo info;
    private double minValue;
    private Bid highestBid;
    private List<Bid> bids;
    private IAuctionClient owner;

    public AuctionItem(int id, String name, double minValue,
            Date endTime, IAuctionClient owner) {
        this.info = new AuctionItemInfo(id, name, endTime);
        this.minValue = minValue;
        this.owner = owner;
        this.bids = new LinkedList<Bid>();
    }

    public AuctionItemInfo getItemInfo() {
        return info;
    }

    public void closeAuction() {
        info.setStatus(AuctionStatus.CLOSED);
    }

    public double getMinValue() {
        return minValue;
    }

    public IAuctionClient getOwner() {
        return owner;
    }

    public void addBid(Bid bid) {
        if (highestBid == null || highestBid.getValue() < bid.getValue()) {
            info.setHighestBid(bid.getValue());
            highestBid = bid;
        }
        
        bids.add(bid);
    }

    public Collection getBids() {
        return Collections.unmodifiableList(bids);
    }

    public Bid getHighestBid() {
        return highestBid;
    }
}
