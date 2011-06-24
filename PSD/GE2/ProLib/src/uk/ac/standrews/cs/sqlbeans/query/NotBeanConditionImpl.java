package uk.ac.standrews.cs.sqlbeans.query;

public class NotBeanConditionImpl<T> implements NotBeanCondition<T> {
	
	private BeanCondition<T> operand;

	public NotBeanConditionImpl (BeanCondition<T> operand){
		this.operand = operand;
	}
	
	@Override
	public String toSQLFormat() {
		return " NOT ("+operand.toSQLFormat()+") ";
	}

}
