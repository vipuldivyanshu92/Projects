package uk.ac.standrews.cs.sqlbeans;

public final class SQLBeanLogging {

	
	public static String logSQL(String message, String statement){
		 return message+" with statement ["+(statement==null?"unknown":statement)+"].";
	}
}
