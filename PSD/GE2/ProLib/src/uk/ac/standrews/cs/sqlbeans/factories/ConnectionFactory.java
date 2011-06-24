package uk.ac.standrews.cs.sqlbeans.factories;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;


public class ConnectionFactory {
	
	//private static final String DB_CONFIG_FILENAME = "config/db.properties";
	
	private static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(ConnectionFactory.class);
	
	private String username;
	private String password;
	private String url;

	private String dbname;

	private String driver;
	
	public ConnectionFactory (String config_file){
		Properties p = new Properties();
		try {
			p.load(new FileInputStream(config_file));
		} catch (FileNotFoundException e) {
			logger.error("Couldn't locate database configuration file ["+config_file+"].",e);
		} catch (IOException e) {
			logger.error("While loading database configuration file ["+config_file+"].",e);
		}
		
		this.username = p.getProperty("username");
		this.password = p.getProperty("password");
		this.dbname = p.getProperty("dbname");
		this.url = p.getProperty("url");	
		this.driver = p.getProperty("driver");
		
		if (driver == null){
			logger.fatal("No SQL driver specified.");
			return;
		}
		try {
			logger.debug("Checking driver ["+driver+"]....");
			Class.forName(p.getProperty("driver"));		
		} catch (ClassNotFoundException e) {
			logger.error("Couldn't locate JDBC driver ["+p.getProperty("driver")+"]",e);
		}
	}

	public Connection createConnection() {	
		logger.debug("Creating connection for end point ["+url+"] and database ["+dbname+"] with username ["+username+"] and password ["+password+"].");
		Connection connection = null;
		try {
			String conn = ""+url;
			if (dbname != null) conn+="/"+dbname;
			
			connection = DriverManager.getConnection(conn, username, password);
			
		} catch (SQLException e) {
			logger.error("Couldn't create connection for specified url ["+url+"].",e);
		}		
		return connection;
	}

	public void closeConnection(Connection connection) {
		try {
			connection.close();
		} catch (SQLException e) {
			logger.error("Whilst trying to close connection ["+connection+"] to database.");
		}
	}
}
