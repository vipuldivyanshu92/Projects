package uk.ac.standrews.cs.sqlbeans;

import java.sql.Connection;
import java.sql.ResultSet;
import java.util.List;
import java.util.Set;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.standrews.cs.sqlbeans.factories.ConnectionFactory;
import uk.ac.standrews.cs.sqlbeans.query.BeanCondition;
import uk.ac.standrews.cs.sqlbeans.util.BeanToDBUtil;
import uk.ac.standrews.cs.sqlbeans.util.DBTablesUtil;
import uk.ac.standrews.cs.sqlbeans.util.DBToBeanUtil;
import uk.ac.standrews.cs.sqlbeans.util.SQLStatementsUtil;

public class DatabaseWrapper {
	
	private static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(DatabaseWrapper.class);
	
	private ConnectionFactory cf;
	
	public DatabaseWrapper (ConnectionFactory cf){
		this.cf = cf;		
	}
	
	public void createTables(Set<Class<?>> bean_types){
		Connection connection = cf.createConnection();
		for (Class<?> bean_type: bean_types)
			DBTablesUtil.createTable(connection,bean_type);
		cf.closeConnection(connection);
	}

	public void createTable(Class<?> bean_type){
		Connection connection = cf.createConnection();
		DBTablesUtil.createTable(connection, bean_type);
		cf.closeConnection(connection);
	}

	public void dropTables(List<Class<?>> tables){
		Connection connection = cf.createConnection();
		for (Class<?> table: tables) DBTablesUtil.dropTable(connection, table);
		cf.closeConnection(connection);
	}

	public void dropTable(Class<?> table){
		Connection connection = cf.createConnection();
		DBTablesUtil.dropTable(connection, table);
		cf.closeConnection(connection);
	}
	
	public <T> List<T> getEntitySet(BeanCondition<T> bean_condition, Class<? extends T> bean_type){
		String query = SQLStatementsUtil.createSelectStatement(bean_type, bean_condition);
		return getEntitySet(query,bean_type);
	}
	
	public <T> List<T> getEntitySet(String query, Class<? extends T> bean_type){
		List<T> beans = null;
		Connection connection = cf.createConnection();
		ResultSet resultset = SQLStatementsUtil.getResultSet(connection,query);
		beans = DBToBeanUtil.getEntitySet(resultset, bean_type);
		cf.closeConnection(connection);
		return beans;
	}
		
	public <T> void insertBeans(Class<T> table, List<T> beans){
		Connection connection = cf.createConnection();
		for (T bean: beans)	BeanToDBUtil.insertBean(connection,table,bean);
		cf.closeConnection(connection);
	}
	
	public <T> void insertBean(Class<T> table, T bean){
		Connection connection = cf.createConnection();
		BeanToDBUtil.insertBean(connection,table,bean);
		cf.closeConnection(connection);
	}
	
	/**
	 * Executes an update 
	 * @param table the identifier of the database table to be updated
	 * @param bean the values to be updated in the table.  Null values are ignored.
	 * @param condition the condition by which the table rows are updated.
	 * @param <T> the bean type to be updated.
	 */
	public <T> void updateBeans(Class<T> table, T bean, BeanCondition<T> condition){
		Connection connection = cf.createConnection();
		BeanToDBUtil.alterBeans(connection,table,bean,condition);
		cf.closeConnection(connection);		
	}
	
	/**
	 * Deletes all entries in the specified tables where the column values for that entry match 
	 * all of the instantiated properties of at least one bean in the provided list.  The list of
	 * beans can be thought of as a disjunction (the list) of conjunctions (each individual bean)
	 * for the condition of an SQL delete statement.
	 * @param <T> The bean type to be inspected.
	 * @param table The table to delete
	 * @param condition the programmatic representation of the bean condition.
	 */
	public <T> void deleteBeans(String table, BeanCondition<T> condition) {
		Connection connection = cf.createConnection();
		BeanToDBUtil.deleteBeans(connection,table,condition);
		cf.closeConnection(connection);		
	}

	public <T> T getBeanByID(Class<? extends T> beanType, Integer ID) {
		logger.debug("Searching for bean in table ["+beanType.getSimpleName()+"] with ID ["+ID+"].");
		
		QueryTranslator<T> queryTranslator = new QueryTranslator<T>(beanType);
 		BeanCondition<T> beanCondition = queryTranslator.resolveQuery("ID='"+ID+"'\n");
 		List<T> beans = getEntitySet(beanCondition, beanType);
 		T bean = beans.size()>0?beans.get(0):null;
 		logger.debug("Found bean ["+bean+"].");
 		return bean;
	}
}
