package auctionsystem.shared;

import java.io.Serializable;
import java.util.Date;

/**
 *
 * @author Adraen
 */
public class AuctionItemInfo implements Serializable {
    private int id;
    private String name;
    private AuctionStatus status;
    private double highestBid;
    private Date endTime;

    public AuctionItemInfo(int id, String name, Date endTime) {
        this.id = id;
        this.name = name;
        this.endTime = endTime;
        this.status = AuctionStatus.OPEN;
    }

    // Setters
    public void setStatus(AuctionStatus status) {
        this.status = status;
    }

    public void setHighestBid(double value) {
        this.highestBid = value;
    }

    // Getters
    public int getId() {
        return this.id;
    }

    public String getName() {
        return this.name;
    }

    public AuctionStatus getStatus() {
        return this.status;
    }

    public double getHighestBid() {
        return this.highestBid;
    }

    public Date getEndTime() {
        return this.endTime;
    }
}
