package uk.ac.standrews.cs.sqlbeans.query;

import java.util.List;

import uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil;
import uk.ac.standrews.cs.sqlbeans.util.TypeMapperUtil;

import static uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil.*;

public class AtomicBeanConditionImpl<T> implements AtomicBeanCondition<T> {
	
	private T bean;
	private Class<? extends T> beanType;
	
	public AtomicBeanConditionImpl(T bean, Class<? extends T> beanType){
		this.bean = bean;
		this.beanType = beanType;
	}
	
	public String toSQLFormat (){
		return createCondition(bean);
	}
	
	private String createCondition (T bean){
		StringBuffer sb = new StringBuffer();

		if (bean != null){	
			List<String> columns = TypeMapperUtil.getFieldNames(bean.getClass());
					
			for (String column: columns){
				Object value = invokeGetMethod(bean, column);
				if (value !=null){
					sb.append(" ( ");
					sb.append(column).append(" LIKE \'");
					
					Class<?> propertyType = ReflectionUtil.getPropertyType(beanType, column);
					
					if (TypeMapperUtil.isIndexedBeanClass(propertyType)){
						Object ID = ReflectionUtil.invokeGetMethod(value, "ID");
						sb.append(ID.toString());
					} else {
						sb.append(value.toString());
					}
					sb.append("\' ) AND ");

				}
			}
		}
		if (sb.length()> 0) sb.append(" ( TRUE  ) ");
		else sb.append("( FALSE )");
		return sb.toString();
	}
}