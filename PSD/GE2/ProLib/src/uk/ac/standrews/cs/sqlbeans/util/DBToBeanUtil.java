package uk.ac.standrews.cs.sqlbeans.util;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

public class DBToBeanUtil {
	
	private static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(DBToBeanUtil.class);
	
	public static <T> List<T> getEntitySet(ResultSet resultset, Class<? extends T> bean_class) {
		List<T> beans = new ArrayList<T>();
		BeanFactory bf = new BeanFactory();
		try {
			while (resultset.next()){
				Map<String,Object> bean_properties = DBToBeanUtil.getRowValues(resultset,bean_class);
				T bean = bf.createNewBean(bean_properties,bean_class);
				logger.debug("Created new bean ["+bean+"] for class ["+bean_class.getSimpleName()+"]");
				beans.add(bean); 
			}
		} catch (SQLException e) {
			logger.error("While parsing database query result into a bean list.",e);
		}
		return beans;
	}

	
	public static <T> Map<String,Object>  getRowValues(ResultSet resultset, Class<? extends T> bean_class){
		logger.debug("Obtaining properties for ["+bean_class+"] from resultset ["+resultset+"].");
		Map<String,Object> result = new HashMap<String,Object>();
		
		for (String col_label: TypeMapperUtil.getFieldNames(bean_class)){	
			try {
				int col_index = 0;
				try {
					col_index = resultset.findColumn(col_label);
				} catch(SQLException e){continue;}
				
				if (col_index < 1) continue;
				
				Class<?> column_type = Class.forName(resultset.getMetaData().getColumnClassName(col_index));
				Class<?> property_type = ReflectionUtil.getPropertyType(bean_class, col_label);
				
				if (TypeMapperUtil.isIndexedBeanClass(property_type)){
					Integer ID = resultset.getInt(col_index);
					Connection connection = resultset.getStatement().getConnection();
					Map<String,Object> values = getRowValues(connection,col_label,property_type,ID);
					result.put(col_label, values);
					
				}else {
					Object arg = getArgumentByParameterType(resultset, col_index, column_type);	
					if (arg != null)result.put(col_label, arg);
				}
			} catch (SQLException e) {
				logger.error("Error inspecting result set columns.",e);
			} catch (ClassNotFoundException e) {
				logger.error("Couldn't get class type.",e);
			}
		}
		return result;
	}
	
	private static <T> Map<String,Object> getRowValues(Connection connection, String property, Class<? extends T> property_type, Integer ID){
		
		//Should produce a single row.
		ResultSet resultset = SQLStatementsUtil.getTableRowByID(connection, property_type, ID);
		
		boolean ready = false; 
		try {
			ready = resultset.next();
		} catch (SQLException e) {
			logger.error("Couldn't determine state of result set.",e);
		}
		if (ready) return getRowValues(resultset,property_type);
		else return new HashMap<String,Object>();	
	}
	
	private static Object getArgumentByParameterType (ResultSet resultset, int column, Class<?> partype) throws SQLException{
		if (partype == String.class){
			String value =  resultset.getString(column);
			logger.debug("Returning String value ["+value+"] for column ["+column+"]." );
			return value;
		} else if (partype == Long.class){
			Long value = resultset.getLong(column);
			logger.debug("Returning Long value ["+value+"] for column ["+column+"]." );
			return value;
		} else if (partype == Integer.class){
			Integer value = resultset.getInt(column);
			logger.debug("Returning Integer value ["+value+"] for column ["+column+"]." );
			return value;
		}
		else return null;
	}
}
