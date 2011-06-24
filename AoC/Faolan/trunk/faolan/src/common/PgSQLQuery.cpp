/*
Faolan Project, a free Age of Conan server emulator made for educational purpose
Copyright (C) 2008 Project Faolan team

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

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

