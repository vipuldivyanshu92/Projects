package uk.ac.standrews.cs.sqlbeans.query;

public class AndBeanConditionImpl<T> implements AndBeanCondition<T> {

	private BeanCondition<T> left;
	private BeanCondition<T> right;

	public AndBeanConditionImpl (BeanCondition<T> left, BeanCondition<T> right){
		this.left = left;
		this.right = right;		
	}
	
	@Override
	public String toSQLFormat(){
		return left.toSQLFormat()+" AND "+right.toSQLFormat();
	}
}
