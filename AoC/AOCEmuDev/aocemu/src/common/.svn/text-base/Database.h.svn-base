#ifndef DATABASE_H_
#define DATABASE_H_

#include <boost/thread.hpp>
#include <boost/foreach.hpp>
#include <boost/bind.hpp>
#include <boost/function.hpp>
#include <queue>
#include <vector>

#include "Common.h"
#include "SafeQueue.h"

class Query;
/**
 * Management of a set of database connexion each executed in a different thread
 * The architecture of the following class is close to the ThreadPool pattern.
 * ex:
 * 1 thread per DB connection (worker threads)
 * Database enqueue queries (tasks)
 * Tasks can have callback methods executed in the connection thread or in the thread running the database
 * @author Albator
 */
class Database {
public:

    Database(std::size_t poolConnSize);

    class DatabaseConnection {
public:

        DatabaseConnection(Database* db);

        virtual bool connected() = 0;

        virtual bool disconnect() = 0;

        virtual ~DatabaseConnection()
        {
        }
        
        void run();

        void processQuery(Query* q);
        
        Database* m_db;
        
        virtual void shutdown()=0;

protected:
        virtual bool dbInitialize() = 0;

        mutable boost::mutex m_mutex;
        boost::condition m_condition;
        bool m_connected, m_shutdown;
        Query* m_query;
       
        

    };

    /**
     * add a query to the queue
     * executed when a connection thread is available
     */
    void enqueueQuery(Query* q);

    /**
     * consumed query, can have a callback function executed later in the main thread
     */
    void enqueueFinishedQuery(Query* q);
    
    
    /**
     * Start database thread
     */
    virtual void start()=0;
    
    /**
     * Loop through the finished query to execute their callback in the main thread (calling thread)
     * 
     */
    void runFinishedQueryCallback();
    
    /**
     * release a connection to the pool
     */
    void releaseDBConnection(DatabaseConnection* db);
    
    
    /**
     * @return number of available DB in the pool
     */
    std::size_t availableDBConnection();

    virtual ~Database()
    {

    }
    
    /**
     * Shutdown database thread and all the thread in the pool
     * delete connections to db
     */
    void shutdown();

protected:

    virtual void dbInitialize()=0;
    
    /**
     * Start all connection threads
     * main database loop, wait for new task.
     */
    void run();

    SafeQueue<DatabaseConnection*> m_dbConnQueue;
    SafeQueue<Query*> m_queryQueue;
    SafeQueue<Query*> m_executedQueryQueue;
    std::size_t m_poolConnSize;
    boost::thread_group m_group;
    bool m_shutdown;
    std::vector<DatabaseConnection*> m_dbConn;
    boost::thread *m_runThread;
    
    

};
#endif /*DATABASE_H_*/
