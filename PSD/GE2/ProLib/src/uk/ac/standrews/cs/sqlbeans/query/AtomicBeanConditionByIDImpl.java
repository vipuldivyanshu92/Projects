package uk.ac.standrews.cs.sqlbeans.query;

import static uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil.invokeGetMethod;

public class AtomicBeanConditionByIDImpl<T> implements AtomicBeanCondition<T> {

	private T bean;
	
	public AtomicBeanConditionByIDImpl(T bean) {
		this.bean = bean;
	}

	@Override
	public String toSQLFormat() {
		return createCondition (bean);
	}
	
	private static <T> String createCondition (T bean){
		StringBuffer sb = new StringBuffer();

		if (bean != null){	
			Object value = invokeGetMethod(bean, "ID");
			if (value !=null){
				sb.append(" ( ");
				sb.append("ID").append("=").append(value.toString());
				sb.append(" ) ");
			}
		}
		
		if (sb.length() == 0) sb.append("( FALSE )");
		return sb.toString();
	}

}
