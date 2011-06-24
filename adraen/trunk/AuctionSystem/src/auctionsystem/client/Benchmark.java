
package auctionsystem.client;

import auctionsystem.shared.IAuctionServer;
import java.rmi.Naming;
import java.util.Calendar;
import java.util.Date;
import java.util.Random;

/**
 *
 * @author 0704887j
 */
public class Benchmark {
    private static Random rand = new Random();

    private static String getRandString(int length) {
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < length; i++)
            sb.append((char)(rand.nextInt(26) + 97));

        return sb.toString();
    }

    public static void main(String argv[]) {
        try {
            // Connect to the auction server
            IAuctionServer server = (IAuctionServer)Naming.lookup("rmi://localhost:1099/AuctionServer");

            // Create an instance of the auction client
            AuctionClient client = new AuctionClient();

            //
            Calendar c = Calendar.getInstance();
            c.add(Calendar.MINUTE, 10);

            // Create n auctions
            server.createAuction(getRandString(8), rand.nextInt(100), c.getTime(), client);
            for (int i = 0; i < 10000; i++)
                server.createAuction(getRandString(8), rand.nextInt(100), c.getTime(), client);

            server.getAuctionItems();
            // Time to query it 100 times
            Date start = new Date();
            for (int i = 0; i < 100; i++)
                server.getAuctionItems();
            Date end = new Date();

            System.out.println(end.getTime() - start.getTime());

            // Exit, callback operations can be pending
            System.exit(0);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
