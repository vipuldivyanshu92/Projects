#include "PgSQLQuery.h"
#include "PgSQLDatabase.h"

PgSQLQuery::PgSQLQuery(QueryType t) :
    Query(t), m_res(NULL), m_rowIdx(-1), m_row(0)
{

}

PgSQLQuery::PgSQLQuery(boost::function<void ()> f, CallbackType type, QueryType t) :
    Query(f, type, t), m_res(NULL), m_rowIdx(-1), m_row(0)
{

}

PgSQLQuery::PgSQLQuery(CallbackType type, QueryType t) :
    Query(type, t), m_res(NULL), m_rowIdx(-1), m_row(0)
{

}

bool PgSQLQuery::execute()
{
    if (m_dbc)
    {
        PgSQLDatabase::PgSQLDatabaseConnection* mydbc =
                (PgSQLDatabase::PgSQLDatabaseConnection*)m_dbc;

        m_res = PQexec(mydbc->m_pgsql, m_queryTxt);
        if (PQresultStatus(m_res)==PGRES_COMMAND_OK)
        {
            return true;
        }
    }

    return false;
}

bool PgSQLQuery::storeResult()
{
    if (m_dbc)
    {
        PgSQLDatabase::PgSQLDatabaseConnection* mydbc =
                (PgSQLDatabase::PgSQLDatabaseConnection*)m_dbc;
        
        m_res = PQexec(mydbc->m_pgsql, m_queryTxt);
        if (PQresultStatus(m_res)==PGRES_TUPLES_OK)
        {
            m_column= PQnfields(m_res);
            m_row = PQntuples(m_res);
            
            return true;
        }

    }
    return false;
}

bool PgSQLQuery::fetchRow()
{
    if (m_res)
    {
        m_rowIdx++;
        if(m_rowIdx >= m_row)
        {
            return false;
        }

    }

    return true;
}

std::string PgSQLQuery::error()
{
    if (m_dbc)
    {
        PgSQLDatabase::PgSQLDatabaseConnection* mydbc =
                (PgSQLDatabase::PgSQLDatabaseConnection*)m_dbc;
        return PQerrorMessage(mydbc->m_pgsql);
    }

    return "";

}

//////////////////////////////////////////////////////
// get returned values from query
//
////////////////////////////////////////////////////////


uint32 PgSQLQuery::getUint32(uint32 idx)
{
    if (m_res && (idx < m_column))
    {
        m_idx++;
        return atoi(PQgetvalue(m_res,m_rowIdx,idx));
    }

    return NULL;
}

uint64 PgSQLQuery::getUint64(uint32 idx)
{
    if (m_res && (idx < m_column))
    {
        m_idx++;
        return boost::lexical_cast<uint64>(PQgetvalue(m_res,m_rowIdx,idx));
    }

    return NULL;
}

const char* PgSQLQuery::getString(uint32 idx)
{
    if (m_res && (idx < m_column))
    {
        m_idx++;
        return PQgetvalue(m_res,m_rowIdx,idx);
    }

    return NULL;
}

uint32 PgSQLQuery::getUint32()
{
    return getUint32(m_idx);
}

uint64 PgSQLQuery::getUint64()
{
    return getUint64(m_idx);
}

const char* PgSQLQuery::getString()
{
    return getString(m_idx);
}

