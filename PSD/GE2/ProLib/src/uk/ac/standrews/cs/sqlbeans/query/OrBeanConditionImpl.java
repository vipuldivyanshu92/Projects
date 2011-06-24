package uk.ac.standrews.cs.sqlbeans.query;

public class OrBeanConditionImpl<T> implements OrBeanCondition<T> {

	
	private BeanCondition<T> left;
	private BeanCondition<T> right;

	public OrBeanConditionImpl (BeanCondition<T> left, BeanCondition<T> right){
		this.left = left;
		this.right = right;		
	}
	
	public String toSQLFormat(){
		return left.toSQLFormat()+" OR "+right.toSQLFormat();
	}

}
