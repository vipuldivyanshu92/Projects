package uk.ac.standrews.cs.l4jconfig;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Properties;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

public class L4JConfiguredLoggerFactory {
	public static final String conf_path = System.getenv("L4J_CONF_FILE");
	
	private static Properties configuration;

	
	private static void doConfiguration(){
		configuration = new Properties();

		URL url = L4JConfiguredLoggerFactory.class.getClassLoader().getResource(conf_path);			
		if (url == null){
			try {
				url = (new File(conf_path)).toURI().toURL();
			} catch (MalformedURLException e) {
				e.printStackTrace();
			}
		} 
			
		try {
			configuration.load(url.openConnection().getInputStream());
		} catch (IOException e) {
			e.printStackTrace();
		}
		PropertyConfigurator.configure(configuration);
	}
	
	public static Logger getConfiguredL4JLogger(Class<?> clazz){
		if (configuration == null) doConfiguration();
		return Logger.getLogger(clazz);
	}
}