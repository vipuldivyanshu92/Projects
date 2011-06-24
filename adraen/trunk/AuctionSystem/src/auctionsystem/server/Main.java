package auctionsystem.server;

import auctionsystem.libraries.Configuration;
import auctionsystem.libraries.Logger;
import java.io.IOException;
import java.io.PrintStream;
import java.rmi.Naming;
import java.rmi.RMISecurityManager;


/**
 * @author Simon Jouet
 */
public class Main {
    private static Configuration config;
    private static Logger logger;

     /**
     * Print the help page
     */
    public static void printHelp() {
        System.out.println("Usage: java auctionsystem.client.Main [OPTION]");
        System.out.println();
        System.out.println("Options:");
        System.out.println("  --help");
        System.out.println("  --file-logging=FILENAME,LOGGING_LEVEL");
        System.out.println("  --stdio-logging=LOGGING_LEVEL");
        System.out.println("  --bind-host=HOSTNAME");
        System.out.println("  --bind-port=PORT");
        System.out.println("  --purge-time=TIME (in minutes)");
        System.out.println("  --no-cache");
        System.out.println();
        System.out.println("Level of logging:");
        for (Logger.LOGGING_LEVEL l : Logger.LOGGING_LEVEL.values())
            System.out.printf("  %s\n", l);
    }

    public static void main(String argv[]) {
        // Retrieve the configuration from the program arguments
        config = Configuration.getInstance();
        config.parseCommandLineArgs(argv);

        // Check if the help need to be printed
        if (config.hasKey("help")) {
            printHelp();
            System.exit(0);
        }

        // Configure the logger
        logger = Logger.getInstance();

        // Check if file logging is required
        if (config.hasKey("file-logging")) {
            String filelevel = config.getString("file-logging", "");
            String[] filelevelpair = filelevel.split(",");
            if (filelevelpair.length == 2) {
                Logger.LOGGING_LEVEL level = null;
                PrintStream ps = null;

                // Get the debug level
                try {
                    level = Logger.LOGGING_LEVEL.valueOf(
                            filelevelpair[1].toUpperCase());
                } catch (Exception e) {
                    System.err.println("Incorrect Logging level");
                }

                // Get the file stream
                try {
                    ps = new PrintStream(filelevelpair[0]);
                } catch (IOException e) {
                    System.err.println("Unable to open the log file");
                }

                // Add the output stream to the logger
                if (level != null && ps != null)
                    logger.addOutputStream(ps, level);
            } else {
                System.err.println("Incorrect file logging format "
                        + "use --file-logging=filename,level");
            }
        }

        // Check if stdio logging is required
        if (config.hasKey("stdio-logging"))
        {
            String stdiolevel = config.getString("stdio-logging", "");
            try {
                Logger.LOGGING_LEVEL level =
                        Logger.LOGGING_LEVEL.valueOf(stdiolevel.toUpperCase());
                logger.addOutputStream(System.out, level);
            } catch (Exception e) {
                System.err.println("Incorrect logging level");
            }
        }

        // Create the security manager
        if (System.getSecurityManager() == null)
            System.setSecurityManager((new RMISecurityManager()));

        try {
            AuctionServer server = new AuctionServer();
            Naming.rebind(String.format("//%s:%s/AuctionServer",
                config.getString("bind-host", "0.0.0.0"),
                config.getString("bind-port", "1099")
            ), server);
            logger.info("AuctionServer is up and running");
        } catch (Exception e) {
            logger.critical("Exception: %s", e.getMessage());
        }
    }
}
