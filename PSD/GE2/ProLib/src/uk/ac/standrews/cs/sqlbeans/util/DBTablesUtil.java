package uk.ac.standrews.cs.sqlbeans.util;

import static uk.ac.standrews.cs.sqlbeans.SQLBeanLogging.logSQL;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

/**
 * Utility class for manipulating database tables via bean classes.
 * @author tws
 */
public class DBTablesUtil {
	
	protected static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(DBTablesUtil.class);
	
	public static <T> void createTable(Connection connection, Class<T> bean_class){
		String table = bean_class.getSimpleName();
		logger.debug("Creating table ["+table+"] on with bean class ["+bean_class+"].");
		String command = SQLStatementsUtil.createCreateTableStatement(table, bean_class);
		try {	
			Statement statement = connection.createStatement();
			statement.execute(command);
			
		} catch (SQLException e) {
			logger.error(logSQL("During creation of table ["+table+"].",command),e);
		}
	}
		
	public static <T> void dropTable(Connection connection, Class<T> bean_class){
		String table = bean_class.getSimpleName();
		logger.debug("Dropping table ["+table+"].");
		try {
			Statement statement = connection.createStatement();
			statement.execute("DROP TABLE "+table);
		}catch(SQLException sqle){
			logger.error(logSQL("During table drop of ["+table+"].",null),sqle);
		}			
	}
}
