package auctionsystem.libraries;

import java.util.HashMap;

/**
 * Simple configuration based on an hashmap and the input arguments
 * @author Simon Jouet
 */
public class Configuration {
    private static Configuration instance = null;
    private HashMap<String, String> config;

    // Singleton constructor
    private Configuration() {
        config = new HashMap<String, String>();
    }

    /**
     * Retrieve the configuration instance
     * @return Configuration object
     */
    public static Configuration getInstance() {
        if (instance == null)
            instance = new Configuration();
        return instance;
    }

    /**
     * Parse the command line arguments passed
     * @param argv an array of argument of the form --arg=value
     * @throws IllegalArgumentException if the arguemnt is incorrect
     */
    public void parseCommandLineArgs(String argv[])
            throws IllegalArgumentException {

        //
        for (String arg : argv) {
            String[] pair = arg.split("=");

            //
            if (pair.length > 2 || !pair[0].startsWith("--") ||
                    pair[0].length() < 3)
                throw new IllegalArgumentException();

            //
            config.put(pair[0].substring(2),
                    pair.length == 2 ? pair[1] : null);
        }
    }

    /**
     * Check if the config as the specified key set
     * @param name key of the config
     * @return true if exists, false otherwise
     */
    public boolean hasKey(String name) {
        return config.containsKey(name);
    }

    /**
     * Retrieve an Integer from the associated key
     * @param name key of the config
     * @param dflt default value
     * @return associated value if the key exists otherwise default
     */
    public int getInt(String name, int dflt) {
        String v = config.get(name);
        if (v != null)
            return Integer.parseInt(v);
        else
            return dflt;
    }

    /**
     * Retrieve a String from the associated key
     * @param name key of the config
     * @param dflt default value
     * @return associated value if the key exists otherwise default
     */
    public String getString(String name, String dflt) {
        String v = config.get(name);
        if (v != null)
            return v;
        else
            return dflt;
    }
}
