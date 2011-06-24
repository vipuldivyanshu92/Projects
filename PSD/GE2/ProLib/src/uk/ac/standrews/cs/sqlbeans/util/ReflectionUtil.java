package uk.ac.standrews.cs.sqlbeans.util;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

/**
 * Utility class for interacting with bean properties via reflection.
 * @author tws
 *
 */
public class ReflectionUtil {
	
	protected static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(ReflectionUtil.class);
		
	/**
	 * Retrieves the specified property from the specified bean.
	 * @param <T>
	 * @param bean the target object.
	 * @param property the identifier of the property to be retrieved.
	 * @return the current value of the specified property.
	 */
	public static <T> Object invokeGetMethod(T bean, String property){
		String method_name = "get"+property;
		return ReflectionUtil.invokeMethod(bean,method_name, new Class[]{},new Object[]{});
	}

	/**
	 * Sets the specified property to the specified value on the target bean.
	 * @param <T> The type of the bean to be adjusted.
	 * @param bean the target object.
	 * @param property the property to be set
	 * @param value the new value for the property.
	 * @param property_type the type of the property to be set (either the type of the value,
	 *  or a super class of, or an interface implemented by the type). 
	 */
	public static <T> void invokeSetMethod(T bean, String property, Object value, Class<?> property_type){
		String method_name = "set"+property;
		ReflectionUtil.invokeMethod(bean,method_name, new Class[]{property_type},new Object[]{value});
	}
	
	private static <T> Object invokeMethod (T target, String method_name, Class<?>[] parameters, Object[] args){
		try {
			logger.debug("Invoking method ["+method_name+"]("+Arrays.toString(parameters)+") on ["+target+"] with arguments ["+Arrays.asList(args)+"].");
			Method m = getMethod(target.getClass(), method_name, parameters);
			return m.invoke(target, args);
		} catch (SecurityException e) {
			logger.error("Couldn't access method ["+method_name+"].",e);
		} catch (IllegalArgumentException e) {
			logger.error("Bad argument for method ["+method_name+"]",e);
		} catch (IllegalAccessException e) {
			logger.error("Couldn't access method ["+method_name+"].",e);
		} catch (InvocationTargetException e) {
			logger.error("Invocation on target caused exception ["+e.getTargetException()+"]. Cause was ["+e.getCause()+"].",e);
		} return null;
	}
	
	/**
	 * Returns the type of the specified property.  Note that the type returned
	 * is that of the property field, not of the current assigned value. 
	 * @param <T> the type of the class under inspection.
	 * @param bean_class the class object to be inspected.
	 * @param property the property to be inspected.
	 * @return a class object representing the type of the specified property field.
	 */
	public static <T> Class<?> getPropertyType(Class<T> bean_class, String property){
		return getMethod(bean_class, "get"+property,new Class<?>[]{}).getReturnType();
	}
	
	private static <T> Method getMethod(Class<T> bean_class, String name, Class<?>[] parameters) {
		Method m = null;
		try {
			m = bean_class.getMethod(name, parameters);
		} catch (SecurityException e) {
			logger.error("Couldn't access method ["+name+"].",e);
		} catch (NoSuchMethodException e) {
			logger.error("Couldn't find method ["+bean_class.getName()+"."+name+"("+Arrays.toString(parameters)+")].",e);
		}
		return m;
	}
}
