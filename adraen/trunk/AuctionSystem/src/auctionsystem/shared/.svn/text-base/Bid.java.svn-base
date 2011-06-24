package auctionsystem.shared;

import java.io.Serializable;

/**
 * Represent a Bid on an auction
 * @author Simon Jouet
 */
public class Bid implements Serializable {
    private String bidderName;
    private String email;
    private double value;
    private IAuctionClient bidder;

    public Bid(String bidderName, String email, double value,
            IAuctionClient bidder) {
        this.bidderName = bidderName;
        this.email = email;
        this.value = value;
        this.bidder = bidder;
    }

    public String getBidderName() {
        return bidderName;
    }

    public String getEmail() {
        return email;
    }

    public double getValue() {
        return value;
    }

    public IAuctionClient getBidder() {
        return bidder;
    }
}
