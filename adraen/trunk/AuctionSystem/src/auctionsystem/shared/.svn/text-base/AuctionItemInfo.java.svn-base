package auctionsystem.shared;

import java.io.Serializable;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Shared informations about an Auction Item
 * @author Simon Jouet
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

    @Override
    public String toString() {
        DateFormat format = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        return String.format("%-10d %-20s %-8s £%-8.2f %s", id, name, status, highestBid,
                format.format(endTime));
    }
}
