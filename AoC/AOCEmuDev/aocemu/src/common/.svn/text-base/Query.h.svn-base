#ifndef QUERY_H_
#define QUERY_H_

#include "Common.h"
#include "Database.h"
#include <boost/bind.hpp>
#include <boost/function.hpp>

/**
 * database query class
 * @author Albator
 */
class Query {

public:
    
    
    enum CallbackType { MAIN_THREAD, WORKER_THREAD, NO_CALLBACK };
    enum QueryType { HAS_RESULT, NO_RESULT };
    
    /**
     * Query with a callback
     * 
     */
    Query(boost::function<void ()> f, CallbackType type, QueryType t);
    
    
    Query(CallbackType type, QueryType t);
    
    
    /**
     * Query without callback
     */ 
    Query(QueryType t);

    /**
     * assign a text to the query
     */
    //void setQueryText(const std::string& queryText);

    /**
     * assign a text to the query C style
     */
    void setQueryText(const char* queryText, ...);

    
    void setCallbackFunction(boost::function<void ()> f);
    
    void setCallbackType(CallbackType type);
    
    /**
     * Query with result set
     */
    virtual bool storeResult()=0;
    
    /**
     * Jump to the next row of the result set or return false
     */
    virtual bool fetchRow()=0;
    
    
    /**
     * Query without result set
     */
    virtual bool execute()=0;
    
    
    /**
     * Release the connection attached to the object query
     * This will call the query callback.
     */
    void releaseDBConnection();
    
    
    /**
     *  Free results.
     * Use this for query object re-use
     */
    virtual void freeResult()
    {

    }

    void setDatabaseConnection(Database::DatabaseConnection* dbc);

    
    ////////////////////////////////////////////////////////
    // Get data from the current row.
    // increment the column index, if no index precised
    //////////////////////////////////////////////////////
    virtual uint32 getUint32()=0;
    virtual uint64 getUint64()=0;
    virtual const char* getString()=0;
    
    virtual uint32 getUint32(uint32 idx)=0;
    virtual uint64 getUint64(uint32 idx)=0;
    virtual const char* getString(uint32 idx)=0;
    
    
    virtual ~Query()
    {

    }
    
    
    
    
    /**
     * 
     * @return last error message
     */
    virtual std::string error()=0;
    
    boost::function<void ()> m_callback;
    CallbackType m_callbackType;
    QueryType m_queryType;

protected:
    uint32 m_columnIdx;
    char m_queryTxt[512];
    Database::DatabaseConnection* m_dbc;
    uint32 m_column;
    int m_idx;
    
    

};

#endif /*QUERY_H_*/
