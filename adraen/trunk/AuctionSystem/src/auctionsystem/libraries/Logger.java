package auctionsystem.libraries;

import java.io.PrintStream;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.LinkedList;

/**
 * Simple Logger with 4 logging level
 * @author Simon Jouet
 */
public class Logger {
    private static Logger instance = null;
    private DateFormat dateFormat;
    private LinkedList<StreamLevelPair> streams;

    // inner class to store a level associated to its stream
    private class StreamLevelPair {
        LOGGING_LEVEL level;
        PrintStream stream;

        public StreamLevelPair(LOGGING_LEVEL level, PrintStream stream) {
            this.level = level;
            this.stream = stream;
        }
    }

    // Enumeration of available logging levels
    public enum LOGGING_LEVEL {
        DEBUG,
        INFO,
        WARNING,
        CRITICAL,
        NONE
    }

    // Singleton constructor
    private Logger()
    {
        dateFormat = new SimpleDateFormat("HH:mm:ss");
        streams = new LinkedList<StreamLevelPair>();
    }

    /**
     * Retrieve the singleton instance
     * @return Logger instance
     */
    public static Logger getInstance()
    {
        if (instance == null)
            instance = new Logger();
        
        return instance;
    }

    /**
     * Add a stream to write to
     * @param stream stream to write to
     * @param level level of logging
     */
    public void addOutputStream(PrintStream stream, LOGGING_LEVEL level)
    {
        streams.add(new StreamLevelPair(level, stream));
    }

    private void print(LOGGING_LEVEL level, String message)
    {
        for (StreamLevelPair slp : streams)
        {
            if (slp.level.compareTo(level) <= 0)
                slp.stream.printf("[%s][%s]%s\n", dateFormat.format(new Date()), level, message);
        }
    }

    private void printf(LOGGING_LEVEL level, String fmt, Object... args)
    {
        for (StreamLevelPair slp : streams)
        {
            if (slp.level.compareTo(level) <= 0)
            {
                slp.stream.printf("[%s][%s]", dateFormat.format(new Date()), level);
                slp.stream.printf(fmt + "\n", args);
            }
        }
    }

    public void info(String message)
    {
        print(LOGGING_LEVEL.INFO, message);
    }

    public void info(String fmt, Object... args)
    {
        printf(LOGGING_LEVEL.INFO, fmt, args);
    }

    public void debug(String message)
    {
        print(LOGGING_LEVEL.DEBUG, message);
    }

    public void debug(String fmt, Object... args)
    {
        printf(LOGGING_LEVEL.DEBUG, fmt, args);
    }

    public void warning(String message)
    {
        print(LOGGING_LEVEL.WARNING, message);
    }

    public void warning(String fmt, Object... args)
    {
        printf(LOGGING_LEVEL.WARNING, fmt, args);
    }

    public void critical(String message)
    {
        print(LOGGING_LEVEL.CRITICAL, message);
    }

    public void critical(String fmt, Object... args)
    {
        printf(LOGGING_LEVEL.CRITICAL, fmt, args);
    }

    public void close() {
        for (StreamLevelPair slp : streams) {
            slp.stream.close();
        }
    }
}
