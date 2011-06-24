package uk.ac.standrews.cs.sqlbeans.util;

import java.lang.reflect.Method;
import java.sql.Types;
import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

public class TypeMapperUtil {

	public static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(TypeMapperUtil.class);
	
	
	public static Class<?> getBeanTypeOfSQLType(int columnType) {
		switch (columnType){
			case (Types.BOOLEAN): return Boolean.class;
			case (Types.INTEGER): return Long.class;
			case (Types.LONGVARCHAR): return String.class;
			default: return null;
		}
	}

	public static int getSQLTypeOfBeanType(Class<?> partype) {
		logger.debug("Comparing ["+partype+"] with ["+
				String.class+","+
				int.class+","+
				Long.class+","+
				Boolean.class+","+
				boolean.class+
				"].");
		if (partype == String.class) return Types.LONGVARCHAR;
		else if (partype == Long.class) return Types.INTEGER;
		else if (partype == Integer.class) return Types.INTEGER;
		else if (partype == int.class) return Types.INTEGER;
		else if (partype == double.class) return Types.DOUBLE;
		else if (partype == float.class) return Types.FLOAT;
		else if (partype == Boolean.class) return Types.BOOLEAN;
		else if (partype == boolean.class) return Types.BOOLEAN;
		//TODO Would be nice to handle enumerations explicitly.
		else if (partype.isEnum()) return Types.LONGVARCHAR;
		//Check if the field is a reference to another table.
		else if (isIndexedBeanClass(partype)) return Types.INTEGER;
		return Types.OTHER;
	}
	
	public static boolean isIndexedBeanClass(Class<?> partype){
		Method m = null;
		try {
			logger.debug("Checking whether ["+partype+"] is reference to another record.");
			m = partype.getMethod("getID");
		} catch (SecurityException e) {
		} catch (NoSuchMethodException e) {
		}
		return (m!=null);	
	}
	
	public static String getSQLTypeOfBeanTypeAsString(Class<?> partype) {
		//TODO Jet flavoured sql types - need to make this more flexible.
		int columnType = getSQLTypeOfBeanType(partype);
		switch (columnType){
			case (Types.LONGVARCHAR): return "TEXT";//"LONG VARCHAR";
			case (Types.INTEGER): return "int";
			case (Types.BOOLEAN): return "bit";
			default: return null;
		}
	}
	
	public static Object parseStringValue(Class<?> proptype, String value){
		if (proptype==String.class) return value;
		else if (proptype==Integer.class) return new Integer(value);
		else return null;
	}
	
	/**
	 * Retrieves the bean properties in the specified class that have SQL 
	 * compatable types.
	 * @param <T> the type of the entity to be inspected.
	 * @param entity the reflected class object of the type to be inspected.
	 * @return a list of SQL type compatable property names for the specified
	 *  bean class.
	 */
	public static <T> List<String> getFieldNames (Class<T> entity){
		//Identity column row labels
		Method[] methods = entity.getMethods();
		List<String> field_names = new ArrayList<String>();
		
		for (int i=0; i< methods.length;i++)
			if (methods[i].getName().startsWith("set") ){
				
				int type = getSQLTypeOfBeanType(methods[i].getParameterTypes()[0]);
				
				logger.debug(
						"Testing bean field for valid type...["
						+type+"] vs ["+Types.LONGVARCHAR+","+Types.INTEGER+"]");
				
				if ((type==Types.LONGVARCHAR)||type==Types.INTEGER|| type==Types.BOOLEAN) {
					String col_label = methods[i].getName().substring(3);
					logger.debug("Identified column label "+col_label);
					field_names.add(col_label);
				}
			}
		return field_names;
	}
}
