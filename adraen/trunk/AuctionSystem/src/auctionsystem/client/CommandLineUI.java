package auctionsystem.client;

import auctionsystem.exceptions.AuctionNotFoundException;
import auctionsystem.exceptions.BidInvalidException;
import auctionsystem.shared.AuctionItemInfo;
import auctionsystem.shared.Bid;
import auctionsystem.shared.IAuctionServer;
import auctionsystem.libraries.Logger;
import java.rmi.RemoteException;
import java.util.Calendar;
import java.util.Collection;
import java.util.Date;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Command line user interface for the auction system client
 * @author Simon Jouet
 */
public class CommandLineUI {
    private AuctionClient client;
    private IAuctionServer server;
    private Scanner scanner;
    private Logger logger;

    public CommandLineUI(AuctionClient client, IAuctionServer server) {
        this.client = client;
        this.server = server;
        scanner = new Scanner(System.in);
        logger = Logger.getInstance();
    }

    /**
     * Prompt the user for a string
     * @param prompt prompt message
     * @param scanner stream to read from
     * @return the string read
     */
    private static String promptString(String prompt, Scanner scanner) {
        System.out.print(prompt);
        return scanner.nextLine();
    }

    /**
     * Prompt the user for an integer
     * @param prompt prompt message
     * @param scanner scanner stream to read from
     * @return the integer read
     */
    private static int promptInt(String prompt, Scanner scanner) {
        System.out.print(prompt);

        while (!scanner.hasNextInt()) {
            scanner.next();
            System.out.print(prompt);
        }

        int v = scanner.nextInt();
        scanner.nextLine();
        return v;
    }

    /**
     * Prompt the user for a double value
     * @param prompt prompt message
     * @param scanner scanner stream to read from
     * @return the double read
     */
    private static double promptDouble(String prompt, Scanner scanner) {
        System.out.print(prompt);

        while (!scanner.hasNextDouble()) {
            scanner.next();
            System.out.print(prompt);
        }

        double v = scanner.nextDouble();
        scanner.nextLine();
        return v;
    }

    /**
     * Prompt the user for a timespan in the format #d#h#m
     * @param prompt prompt message
     * @param scanner scanner stream to read from
     * @return a Date object based on the current time + timespan
     */
    private static Date promptTimeSpan(String prompt, Scanner scanner) {
        Pattern p = Pattern.compile("((\\d*)d)?((\\d*)h)?((\\d*)m)?");
        Matcher m;
        String line;

        // Prompt until proper input
        do {
            System.out.print(prompt);
            line = scanner.nextLine();
            m = p.matcher(line);
        } while (!m.find() || line.length() == 0);


        // Get the calendar current instance
        Calendar c = Calendar.getInstance();
        if (m.group(2) != null)
            c.add(Calendar.DATE, Integer.parseInt(m.group(2)));
        if (m.group(4) != null)
            c.add(Calendar.HOUR, Integer.parseInt(m.group(4)));
        if (m.group(6) != null)
            c.add(Calendar.MINUTE, Integer.parseInt(m.group(6)));

        return c.getTime();
    }

    private static void printMainMenu() {
        System.out.println("1. Create a new Auction");
        System.out.println("2. List open Auctions");
        System.out.println("3. Place a Bid on an Auction");
        System.out.println("4. Quit");
    }

    private void createNewAuctionForm() {
        String name = promptString("Item Name: ", scanner);
        double price = promptDouble("Price: ", scanner);
        Date endtime = promptTimeSpan("End Time (#d#h#m): ", scanner);

        try {
            int id = server.createAuction(name, price, endtime, client);
            System.out.printf("Auction created with id %d\n", id);
        } catch (RemoteException e) {
            System.out.println("Unable to create the Auction");
            logger.warning("Unable to create the Auction: %s", e.getMessage());
        }
    }

    private void placeBidForm() {
        int id = promptInt("Auction ID: ", scanner);
        String name = promptString("Name: ", scanner);
        String email = promptString("Email: ", scanner);
        double amount = promptDouble("Amount: ", scanner);

        try {
            server.placeBid(id, new Bid(name, email, amount, client));
            System.out.println("Bid placed successfully");
        } catch (RemoteException e) {
            System.out.println("Unable to place the bid");
            logger.warning("Unable to place the bid: %s", e.getMessage());
        } catch (AuctionNotFoundException e) {
            System.out.printf("The auction %d does not exist\n", id);
            logger.warning("Attempt to bid on a non existing item: %s",
                    e.getMessage());
        } catch (BidInvalidException e) {
            System.out.printf("Unable to place the bid: %s", e.getMessage());
            logger.warning("Unable to place the bid: %s", e.getMessage());
        }
    }

    private void printAuctionItems() {
        try {
            // Retrieve the collection of AuctionItemInfo from the server
            Collection<AuctionItemInfo> items = server.getAuctionItems();
            System.out.println("Id        | Name               | Status |"
                    + " Price   | End date");
            System.out.println("----------------------------------------"
                    + "------------------------------");

            // Iterate through the AuctionItemInfo
            for (AuctionItemInfo i : items)
            {
                System.out.println(i);
            }
        } catch (RemoteException e) {
            System.out.println("Unable to retrieve the list of items");
            logger.warning("Unable to retrieve the list of items: %s",
                    e.getMessage());
        }
    }

    /**
     * Run a basic User Interface for the auction client
     * @param c AuctionClient to use
     * @param s AuctionServer connected to
     */
    public void run() {       
        int choice;
        do {
            printMainMenu();
            choice = promptInt("Choice: ", scanner);
            switch (choice) {
                case 1:
                    createNewAuctionForm();
                    break;
                case 2:
                    printAuctionItems();
                    break;
                case 3:
                    placeBidForm();
                    break;
            }
        } while (choice != 4);
    }


}
