package uk.ac.standrews.cs.sqlbeans.util;

import static uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil.invokeGetMethod;
import static uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil.invokeSetMethod;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

enum Test {A,B,C};

/**
 * Utility class for setting and inspecting properties on java bean instances.
 * @author tws
 */
public class BeanFactory {
	
	protected static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(BeanFactory.class);
	
	private HashMap<Class<?>,Map<Integer,Object>> beanCache;
	
	public BeanFactory (){
		beanCache = new HashMap<Class<?>,Map<Integer,Object>>();
	}
	
	/**
	 * Constructs a new empty bean of the specified type.  If the type is an interface,
	 * then a suitable implementer is searched for.  A suitable implementer must have 
	 * a nullary constructor. 
	 * The new bean's fields are populated from data in the resultset.
	 * @param <T> - the type of the bean to be returned.
	 * @param resultset - the data source for populating the new bean's fields.
	 * @param bean_class - the class type of bean to be returned.
	 * @return a new bean of type T, with fields populated from the result set.
	 */
	public <T> T createNewBean(Map<String,Object> properties, Class<T> bean_class){
		T bean = createNewEmptyBean(bean_class);
		populateBeanFields(properties,bean);
		return bean;
	}
	
	/**
	 * Constructs a new empty bean of the specified type.  If the type is an interface,
	 * then a suitable implementer is searched for.  A suitable implementer must have 
	 * a nullary constructor.
	 * @param <T> the type of the class to be instantiated
	 * @param beanType the reflected class object of the object to be instantiated.
	 * @return a new default instance of type T
	 */
	private <T> T createNewEmptyBean(Class<T> beanType){
		if (beanType == null) return null;
		
		Class<? extends T> implementer = findImplementer(beanType);
		
		if (implementer == null){
			logger.debug("Couldn't locate a class that implements bean type ["+beanType.getSimpleName()+"]");
			return null;
		}
		
		logger.debug("Attempting to instantiate new bean of type ["+beanType.getSimpleName()+"]" +
				" using implementer ["+implementer.getSimpleName()+"].");
		
		T bean = null;
		try {
			bean = implementer.newInstance();
			} catch (InstantiationException e) {
			logger.debug("Couldn't instantiate bean of type ["+beanType.getSimpleName()+"]",e);
		} catch (IllegalAccessException e) {
			logger.debug("Bean class or 0-ary constructor in-accessible["+beanType+"]",e);
		}
		return bean;
	}
	
	private static <T> Class<? extends T> findImplementer(Class<T> beanType){
		if (beanType.isInterface()){
			Class<? extends T> implementer = null;
			try {
				implementer = (Class<? extends T>) Class.forName(beanType.getName()+"Impl");
			} catch (ClassNotFoundException e) {
				logger.debug("couldn't find implementer class for ["+beanType+"].");
			} return implementer;
		} else return beanType;
	}
	
	private <T> void populateBeanFields(Map<String,Object> map, T bean){
		List<String> col_labels = TypeMapperUtil.getFieldNames(bean.getClass());
		logger.debug("Attempting to set bean properties for ["+col_labels+"].");
		
		for (String col_label: col_labels){
			Object value = map.get(col_label);
			if (value != null)
				populateBeanField(bean,col_label,value);
		}
	}
	
	private <S> void populateBeanField(S bean, String property, Object value){
		Class<?> property_type = getBeanPropertyType(bean,property);
		
		if (property_type != null){
			if (TypeMapperUtil.isIndexedBeanClass(property_type) && value instanceof Map<?,?>){
				Map<String,Object> properties = (Map<String,Object>)value;
				populateReferencedBeanField(bean,properties,property_type,property);
			}else if (property_type.isEnum()){ 
				Object[] enums = property_type.getEnumConstants();
				for (Object enumeration: enums)
					if (enumeration.toString().equals(value.toString()))
						invokeSetMethod(bean,property,enumeration,property_type);
			}else invokeSetMethod(bean, property, value, property_type);	
		}	
	}
	
	private <T> void populateReferencedBeanField(T bean, Map<String,Object> properties, Class<?> property_type, String property){
		Integer ID = (Integer)properties.get("ID");
		
		Map<Integer,Object> referencedBeans = beanCache.get(property_type);
		
		if (referencedBeans == null){
			referencedBeans = new HashMap<Integer,Object>();
			beanCache.put(property_type, referencedBeans);
		}
			
		Object referencedBean = referencedBeans.get(ID);
		if (referencedBean == null){
			referencedBean = createNewBean(properties,property_type);
			referencedBeans.put(ID, referencedBean);
		}
		//Now attempt to add symmetric relation to the referenced bean
		//(bean may not support this)
		//TODO
		
		
		invokeSetMethod(bean,property,referencedBean, property_type);
	}
	
	
	
	private static <T> Class<?> getBeanPropertyType(T bean, String property){
		Class<?> partype = null;
		try {
			partype = bean.getClass().getMethod("get"+property).getReturnType();
		} catch (SecurityException e) {
			logger.warn("Bean class ["+bean.getClass()+"] does not have accessible property ["+property+"].",e);
		} catch (NoSuchMethodException e) {
			logger.warn("Bean class ["+bean.getClass()+"] does not have property ["+property+"].",e);
		}
		return partype;
	}
	
	public static <T> Map<String,Object> inspectBeanFields(T bean){ 
		Map<String,Object> result = new HashMap<String,Object>();
		
		List<String> col_labels = TypeMapperUtil.getFieldNames(bean.getClass());
		for (String col_label: col_labels){
			Object val = invokeGetMethod(bean, col_label);
			if (val != null)
				result.put(col_label,val);
		}
		return result;
	}
}
