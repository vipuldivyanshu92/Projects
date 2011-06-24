#include "Database.h"
#include "Query.h"
#include <iostream>
#include <boost/foreach.hpp>
#include <boost/thread.hpp>

Database::Database(std::size_t poolConnSize) :
    m_poolConnSize(poolConnSize), m_shutdown(false), m_dbConn(poolConnSize)
{

}

void Database::run()
{

    dbInitialize();

    Query* q;
    while (!m_shutdown)
    {
        m_queryQueue.popWait(q);
        
        if(m_shutdown && !q)
        {
            // no remaining connection, we can quit the thread
            return;
        }
        
        DatabaseConnection* dbc;
        m_dbConnQueue.popWait(dbc);
        q->setDatabaseConnection(dbc);
        dbc->processQuery(q);
    }
}

void Database::enqueueQuery(Query* q)
{
    m_queryQueue.push(q);

}

void Database::releaseDBConnection(Database::DatabaseConnection* db)
{
    m_dbConnQueue.push(db);
}

void Database::enqueueFinishedQuery(Query* q)
{
    m_executedQueryQueue.push(q);
}

void Database::runFinishedQueryCallback()
{
    Query* q= NULL;

    m_executedQueryQueue.tryPop(q);
    while (q)
    {
        q->m_callback();
        m_executedQueryQueue.tryPop(q);
    }
}

std::size_t Database::availableDBConnection()
{
    return m_dbConnQueue.size();
}

void Database::shutdown()
{
    m_shutdown=true;

    // send shutdown signal to all connection, and execute last query
    BOOST_FOREACH(DatabaseConnection* dbc, m_dbConn)
    {
        if(dbc)
        {
            
            dbc->shutdown();
        }
        
    }
    
    // all the connections should be shutdown
    m_group.join_all();
    if(m_runThread && m_runThread->joinable())
    {
        m_queryQueue.push(NULL); // null shutdown signal, a bit tricky...
        m_runThread->join();
    }
    

}

/////////////////////////////////////////////////////////////////
// DatabaseConnection def
/////////////////////////////////////////////////////////////////

Database::DatabaseConnection::DatabaseConnection(Database* db) :
    m_db(db), m_connected(false), m_shutdown(false), m_query(NULL)
{

}

void Database::DatabaseConnection::processQuery(Query* q)
{
    boost::mutex::scoped_lock lock(m_mutex);
    m_query=q;
    m_condition.notify_one();
}

void Database::DatabaseConnection::run()
{
    boost::mutex::scoped_lock lock(m_mutex);
    

    if(!dbInitialize())
    {
        std::cout << "can't connect to DB" << std::endl;
        return;
    }
    
    std::cout << "connection running" << std::endl;
    while (!m_query)
    {
        m_condition.wait(lock);
        if (m_query)
        {

            // run query
            if (m_query->m_queryType == Query::HAS_RESULT)
            {
                if (!m_query->storeResult())
                {
                    std::cout << m_query->error() <<std::endl;
                }
            } else
            {
                if (!m_query->execute())
                {
                    std::cout << m_query->error() <<std::endl;
                }
            }

            // run callback and release connection
            if (m_query->m_callbackType==Query::WORKER_THREAD)
            {
                m_query->m_callback();
            } else if (m_query->m_callbackType==Query::MAIN_THREAD)
            {
                m_db->enqueueFinishedQuery(m_query);
            }

            //now release the connection/thread and the current query
            m_db->releaseDBConnection(this);
            m_query=NULL;
        }

        if (m_shutdown)
        {
            std::cout << "shutting down connection" << std::endl;
            return;
        }

    }

}

