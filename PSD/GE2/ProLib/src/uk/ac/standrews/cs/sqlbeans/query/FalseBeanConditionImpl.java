package uk.ac.standrews.cs.sqlbeans.query;

public class FalseBeanConditionImpl<T> implements FalseBeanCondition<T> {
	
	@Override
	public String toSQLFormat() {
		return " FALSE ";
	}

}
