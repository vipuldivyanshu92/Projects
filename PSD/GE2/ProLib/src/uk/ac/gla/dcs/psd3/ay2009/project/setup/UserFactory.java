package uk.ac.gla.dcs.psd3.ay2009.project.setup;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.gla.dcs.psd3.ay2009.project.model.User;
import uk.ac.gla.dcs.psd3.ay2009.project.model.UserImpl;

public class UserFactory {
	private static final Logger logger =  L4JConfiguredLoggerFactory.getConfiguredL4JLogger(UserFactory.class);
	
	/**
	 * Constructs a new list of users with random attributes, obtained from a constant source.
	 * 
	 * @param amount the number of users to generate.
	 * @param probStaff the probability that a user is a member of staff in the range 0-1.
	 * @return
	 */
	public static List<User> createUsersProfile(Integer amount, Double probStaff){
		List<User> users = new ArrayList<User>();
			
		List<String> surnames = getSurnames();
		List<String> forenames = getForenames();
			
		Random r = new Random();
			
		for (int i=0; i < amount; i++){
			String surname = surnames.get(r.nextInt(surnames.size()));
			int numForenames = r.nextInt(3);
			String forename = forenames.get(r.nextInt(forenames.size()));
			for (int j = 0 ; j < numForenames;j++){
				forename+=","+forenames.get(r.nextInt(forenames.size()));
			}
			boolean isStaff = r.nextDouble() < probStaff;
			
				
			User user = new UserImpl(i,surname,forename,isStaff);
			users.add(user);
		}
			
		return users;
	}
	
	private static List<String> getSurnames(){
		return getLinesFromFile("config/surnames.txt");
	}
	
	private static List<String> getForenames(){
		return getLinesFromFile("config/forenames.txt");
		
	}
	
	private static List<String> getLinesFromFile(String fileName){
		List<String> result = new ArrayList<String>();
		BufferedReader reader = getTextFile(fileName);
		if (reader != null)
			try {
				while (reader.ready())
					result.add(reader.readLine().trim());
			} catch (IOException e) {
				logger.error("While reading lines from file ["+fileName+"]");
			}
		return result;
	}
	
	private static BufferedReader getTextFile(String fileName){
		try {
			return new BufferedReader(new InputStreamReader(new FileInputStream(fileName)));
		} catch (FileNotFoundException e) {
			logger.error("Couldn't find user account generation source file ["+fileName+"]");
		}
		return null;
	}

}
