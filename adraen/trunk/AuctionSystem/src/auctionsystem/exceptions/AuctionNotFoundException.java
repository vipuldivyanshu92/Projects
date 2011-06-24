
package auctionsystem.exceptions;

/**
 * Auction cannot be retrieved
 * @author Simon Jouet
 */
public class AuctionNotFoundException extends Exception {
    public AuctionNotFoundException() {
        super();
    }

    public AuctionNotFoundException(String message) {
        super(message);
    }
}
