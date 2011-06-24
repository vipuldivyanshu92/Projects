package auctionsystem.server;

import auctionsystem.libraries.Configuration;
import auctionsystem.shared.AuctionItemInfo;
import java.util.Collection;
import java.util.LinkedList;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Collection of the AuctionItems, this is a singleton
 * @author Simon Jouet
 */
public class AuctionItemCollection {
    private static AuctionItemCollection instance;

    private final ConcurrentHashMap<Integer, AuctionItem> auctions;
    private final Collection<AuctionItemInfo> infoCache;
    private final Object auctionIdLock;
    private int auctionId;
    private boolean enableCaching;

    private AuctionItemCollection() {
        auctions = new ConcurrentHashMap<Integer, AuctionItem>();
        auctionId = 0;
        auctionIdLock = new Object();

        if (Configuration.getInstance().hasKey("no-cache")) {
            infoCache = null;
            enableCaching = false;
        } else {
            infoCache = new LinkedList<AuctionItemInfo>();
            enableCaching = true;
        }
    }

    public static AuctionItemCollection getInstance()
    {
        if (instance == null)
            instance = new AuctionItemCollection();
        return instance;
    }

    /**
     * Thread safe function to retrieve a unique identifier for an auction item
     * @return a unique identifier
     */
    public int getUniqueId() {
        int id;
        synchronized (auctionIdLock) {
            id = auctionId % Integer.MAX_VALUE;
            auctionId++;
        }
        return id;
    }

    /**
     * Add an AuctionItem with the specified identifier
     * @param id auctionItem unique identifier
     * @param item AuctionItem to add
     */
    public void add(int id, AuctionItem item) {
        auctions.put(id, item);

        if (enableCaching) {
            synchronized (infoCache) {
                infoCache.add(item.getItemInfo());
            }
        }
    }

    /**
     * Remove an AuctionItem
     * @param identifier AuctionItem unique identifier
     */
    public void remove(int identifier) {
        auctions.remove(identifier);
    }

    /**
     * Retrieve an AuctionItem
     * @param identifier AuctionItem unique identifier
     * @return AuctionItem retrieved
     */
    public AuctionItem get(int identifier) {
        return auctions.get(identifier);
    }

    /**
     * Return the Collection of cache auctionItemsInfo.
     * This limits the querying to iterate through the entire collection
     * @return Collection of AuctionItemInfo
     */
    public Collection<AuctionItemInfo> getCachedAuctionItemInfo() {
        if (enableCaching)
        {
            synchronized (infoCache) {
                return infoCache;
            }
        } else {
            Collection<AuctionItemInfo> infos =
                    new LinkedList<AuctionItemInfo>();
            
            for (AuctionItem item : auctions.values())
                infos.add(item.getItemInfo());
            
            return infos;
        }
    }

    /**
     * Get an iterator on the collection items
     * @return and Iterator
     */
    public Collection<AuctionItem> getValues() {
        return auctions.values();
    }

    /**
     * Get the size of the collection
     * @return size of the collection
     */
    public int size() {
        return auctions.size();
    }

    /**
     * Rebuilt the cache of auctionItemInfo
     * @info This is of order O(n) where n is the number of elements in the
     * collection.
     */
    public void rebuildCache() {
        if (enableCaching)
        {
            synchronized (infoCache)
            {
                infoCache.clear();
                for (AuctionItem item : auctions.values()) {
                    infoCache.add(item.getItemInfo());
                }
            }
        }
    }
}
