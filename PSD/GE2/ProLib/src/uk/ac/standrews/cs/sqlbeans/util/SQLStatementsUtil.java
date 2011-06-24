package uk.ac.standrews.cs.sqlbeans.util;

import java.lang.reflect.Method;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.standrews.cs.sqlbeans.query.AtomicBeanCondition;
import uk.ac.standrews.cs.sqlbeans.query.AtomicBeanConditionByIDImpl;
import uk.ac.standrews.cs.sqlbeans.query.BeanCondition;

import static uk.ac.standrews.cs.sqlbeans.SQLBeanLogging.logSQL;
import static uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil.invokeGetMethod;

public class SQLStatementsUtil {
	
	public static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(SQLStatementsUtil.class);
	
	public static ResultSet getResultSet(Connection connection, String query){
		ResultSet resultset = null;
		try {
			Statement statement = connection.createStatement();
			statement.execute(query);
			resultset = statement.getResultSet();
			logger.debug(logSQL("result set size is ["+resultset.getRow()+"].",query));
		} catch (SQLException e) {
			logger.error(logSQL("While retrieving entities with query", query) ,e);
		}
		return resultset;
	}
	
	public static <T> ResultSet getTableRowByID(Connection connection, Class<? extends T> bean_type, Integer ID){
		Map<String,Object> properties = new HashMap<String,Object>();
		properties.put("ID", ID);
		T beanExpr = new BeanFactory().createNewBean(properties, bean_type);
		AtomicBeanCondition<T> beanCondition = new AtomicBeanConditionByIDImpl<T>(beanExpr);
		
		
		String query = SQLStatementsUtil.createSelectStatement(bean_type, beanCondition);
		return SQLStatementsUtil.getResultSet(connection, query);
	}
	
	public static <T> String createCreateTableStatement(String table, Class<T> bean_class) {
		StringBuffer command = new StringBuffer("CREATE TABLE "+table+"(");
	
		for (Method method: bean_class.getMethods())
			if (method.getName().startsWith("set")){
				
				Class<?> partype = method.getParameterTypes()[0];
				String sqltype = TypeMapperUtil.getSQLTypeOfBeanTypeAsString(partype);

				String columnName = method.getName().substring(3);
				
				command.append(columnName).append(" ");
				command.append(sqltype).append(",");
				if (columnName.equals("ID"))
					command.append("PRIMARY KEY(").append(columnName).append("),");
				
			}
		
		command = command.deleteCharAt(command.length()-1).append(")");
		return command.toString();
	}
	
	public static <T> String createSelectStatement (Class<?> bean_type, BeanCondition<T> condition){
		StringBuffer sb = new StringBuffer("SELECT * FROM ").append(bean_type.getSimpleName()).append(createWhereCondition(condition));
		return sb.toString();		
	}
	
	public static <T> String createBlankEntityInsertStatement(T bean, Class<? extends T> bean_class){
		StringBuffer sb = new StringBuffer("INSERT INTO ").append(bean_class.getSimpleName()).append(" ");
		return sb.append(buildValuesExpression(bean, bean_class)).toString();
	}
	
	private static <T> String buildValuesExpression(T bean, Class<? extends T> bean_class){
		StringBuffer sb1 = new StringBuffer(" (");
		StringBuffer sb2 = new StringBuffer(" VALUES( ");
		
		List<String> columns = TypeMapperUtil.getFieldNames(bean_class);
		for (int i=0; i < columns.size();i++){
			String column = columns.get(i);
			Object value = invokeGetMethod(bean,column);
			if(value != null){
				sb1.append(columns.get(i)+(i==columns.size()-1?") ":","));
				sb2.append(i==columns.size()-1?"?)":"?,");
			}
		}
		return sb1.append(sb2).toString();
	}
	
	public static <T> String createBlankEntityUpdateStatement(T bean, Class<? extends T> bean_class, BeanCondition<T> condition){
		StringBuffer sb = new StringBuffer("UPDATE ").append(bean_class.getSimpleName()).append(" SET ");
		sb.append(buildSetExpression(bean,bean_class));
		return sb.append(" WHERE ").append(condition.toSQLFormat()).toString();	
	}
	
	private static <T> String buildSetExpression(T bean, Class<? extends T> bean_class){
		StringBuffer sb = new StringBuffer(" ");
		List<String> columns = TypeMapperUtil.getFieldNames(bean_class);
		
		for (int i=0; i < columns.size();i++){
			String column = columns.get(i);
			Object value = invokeGetMethod(bean,column);
			if(value != null)
				sb.append(column).append("=?, ");
		}
				
		return sb.deleteCharAt(sb.length()-2).append(" ").toString();
	}
	
	public static void insertValueInPreparedStatement(Object value,	Class<?> partype, PreparedStatement ps, int i) {
		logger.debug("Inserting value ["+value+"] of type ["+partype+"] into prepared statement at position ["+i+"].");
		try {
			if (partype.equals(String.class)) ps.setString(i, (String)value);
			else if (partype.isEnum()) ps.setString(i, value.toString());
			else if (partype.equals(Integer.class)) ps.setInt(i, (Integer)value);
			else if (partype.equals(int.class)) ps.setInt(i, (Integer)value);
			else if (partype.equals(Long.class)) ps.setLong(i, (Long)value);
			else if (partype.equals(Boolean.class)) ps.setBoolean(i, (Boolean)value);
			else if (partype.equals(boolean.class)) ps.setBoolean(i, (Boolean)value);
			
		} catch (SQLException e) {
			logger.error(logSQL("couldn't add value ["+value+"] of type ["+partype+"] at position ["+i+"].",ps.toString()));
		}	
	}

	public static <T> String createEntityDeleteStatement(String table, BeanCondition<T> condition) {
		StringBuffer sb = new StringBuffer("DELETE FROM ").append(table).append(createWhereCondition(condition));
		return sb.toString();
	}

	private static <T> String createWhereCondition (BeanCondition<T> condition){
		return " WHERE ( "+condition.toSQLFormat()+" ) ";
	}
}
