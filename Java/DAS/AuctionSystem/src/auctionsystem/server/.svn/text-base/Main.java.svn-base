package auctionsystem.server;

import auctionsystem.shared.AuctionItemInfo;
import auctionsystem.shared.Bid;
import java.util.LinkedList;


/**
 *
 * @author Adraen
 */
public class Main {
    public static void main(String argv[]) {
        AuctionItemInfo info;
        AuctionItem item = new AuctionItem(1, "item", 10, null, null);
        info = item.getItemInfo();

        item.addBid(new Bid("SJ", "email", 10, null));
        System.out.println(info.getHighestBid());

        item.addBid(new Bid("SJ", "email", 20, null));
        System.out.println(info.getHighestBid());

        item.addBid(new Bid("SJ", "email", 3, null));
        System.out.println(info.getHighestBid());
    }
}
