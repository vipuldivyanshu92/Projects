package uk.ac.standrews.cs.sqlbeans.util;

import static uk.ac.standrews.cs.sqlbeans.SQLBeanLogging.logSQL;
import static uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil.invokeGetMethod;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.standrews.cs.sqlbeans.query.BeanCondition;

public class BeanToDBUtil {
	
	protected static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(BeanToDBUtil.class);
	
	public static <T> void alterBeans(Connection connection, Class<T> bean_type, T bean,BeanCondition<T> condition){
		logger.debug("Altering beans of type ["+bean_type.getSimpleName()+"]"+
				" according to condition ["+condition.toSQLFormat()+"].");

		PreparedStatement ps = null;
		String sql_statement = SQLStatementsUtil.createBlankEntityUpdateStatement(bean, bean_type, condition);
		try {
			
			ps = connection.prepareStatement(sql_statement);
			insertValuesInPreparedStatement(ps, bean, bean_type);
			ps.execute();
			
		} catch (SQLException e) {
			logger.error(logSQL("while altering an entry to table ["+bean_type+"]",sql_statement), e);
		}
	}
	
	public static <T> void insertBean(Connection connection,Class<? extends T> bean_type, T bean){

		//Check if the bean has already been inserted.
		Integer ID = (Integer)ReflectionUtil.invokeGetMethod(bean, "ID");
		ResultSet resultset = SQLStatementsUtil.getTableRowByID(connection, bean_type, ID);
		List<T> beans = DBToBeanUtil.getEntitySet(resultset, bean_type);
		if (beans.size() > 0) return;
		
		logger.debug("Inserting new bean of type ["+bean_type+"].");	
		PreparedStatement ps = null;
		try {
			String sql_statement = SQLStatementsUtil.createBlankEntityInsertStatement(bean,bean_type);
			
			ps = connection.prepareStatement(sql_statement);
			insertValuesInPreparedStatement(ps, bean, bean_type);
			
			logger.debug(logSQL("Inserting new entry into ["+bean_type+"]", sql_statement));
			ps.execute();
					
		} catch (SQLException e) {
			logger.error(logSQL("while adding an entry to table ["+bean_type+"]",ps.toString()), e);
		}	
	}
	
	public static <T> void deleteBeans(Connection connection, String table, BeanCondition<T> condition) {
		String sql_statement = null;
		try {
			sql_statement =  SQLStatementsUtil.createEntityDeleteStatement(table,condition);
			
			Statement s = connection.createStatement();
			
			logger.debug(logSQL("Deleting entries in ["+table+"]", sql_statement));
			s.execute(sql_statement);
					
		} catch (SQLException e) {
			logger.error(logSQL("Whilst deleting entries in ["+table+"]",sql_statement), e);
		}				
	}	
		
	private static <T> void insertValuesInPreparedStatement(PreparedStatement ps, T bean, Class<? extends T> bean_type){
		logger.debug("Inserting values from ["+bean+"] into prepared statement.");
		List<String> columns = TypeMapperUtil.getFieldNames(bean_type);
		
		int sql_column = 1;
		for (String column: columns){
			Object value = invokeGetMethod(bean,column);
			
			if (value!=null){		
				Class<?> type = ReflectionUtil.getPropertyType(bean_type,column);
				
				if (TypeMapperUtil.isIndexedBeanClass(type)){
					//Recurse the insert if field is a reference into another table.
					try {
						Connection connection = ps.getConnection();
						insertBean(connection, type, value);
					} catch (SQLException e) {
						logger.error("Couldn't get connection to insert referenced record ["+value+"]");
					}
					
					Object id = ReflectionUtil.invokeGetMethod(value, "ID");
					SQLStatementsUtil.insertValueInPreparedStatement(id,Integer.class,ps,sql_column);	
				} else {
					SQLStatementsUtil.insertValueInPreparedStatement(value,type,ps,sql_column);	
				}
				sql_column++;
			}
		}
	}
}
