package uk.ac.gla.dcs.psd3.ay2009.project.setup;

import java.sql.Connection;
import java.util.List;

import org.apache.log4j.Logger;

import uk.ac.gla.dcs.psd3.ay2009.project.model.Book;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookDescription;
import uk.ac.gla.dcs.psd3.ay2009.project.model.User;
import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.standrews.cs.sqlbeans.DatabaseWrapper;
import uk.ac.standrews.cs.sqlbeans.factories.ConnectionFactory;

/**
 * A utility class for initialising the Central Library database from a
 * specified source configuration. Invocation can occur either via a console 
 * invocation of the class, or via a programmatic call to initialiseDB()
 * on an instance of SetupDB configured at initialisation time.
 * @author tws
 * 
 */
public class SetupDB{
	
	private final Logger logger =  L4JConfiguredLoggerFactory.getConfiguredL4JLogger(SetupDB.class);
	private DatabaseWrapper dbw;

	private Integer numUsers;
	private Integer maxBookCopies;
	private Integer numBooks;
	private String dbConfFileName;
	
	/** The user accounts used to initialise the database User table */
	private List<User> users;
	
	/** The books (with references to descriptions) used to initialise the database */
	private List<Book> books;
	
	/** The probability that a user is a member of staff in the range 0-1.*/
	private Double probStaff;
	
	/**
	 * Provides a console interface to the initialisation script.
	 * @param args
	 */
	public static void main (String[] args){
		SetupDB setupDB = new SetupDB(
				args[0],
				Integer.parseInt(args[1]),
				Double.parseDouble(args[2]),
				Integer.parseInt(args[3]));
		
		setupDB.initialiseDB();
	}

	/**
	 * Configures the setup script according to the constructor parameters.
	 * @param dbConfFileName
	 * @param numUsers
	 * @param probStaff the probability that a user is a member of staff in the range 0-1.
	 * @param numBooks
	 */
	public SetupDB (String dbConfFileName, Integer numUsers, Double probStaff,Integer numBooks){
		this.numUsers = numUsers;
		this.probStaff = probStaff;
		this.numBooks = numBooks;
		this.dbConfFileName = dbConfFileName;
	}
	
	/**
	 * Generates a book and user database according to the configuration of this 
	 * setup instance.  The list of book and user objects used to initialise the database
	 * are retained.
	 */
	public void initialiseDB(){
		
		logger.info("Initialising database ["+dbConfFileName+"]with:" +
				"["+numUsers+"] randomly generated users,\n" +
				"and ["+numBooks+"] number of books"+
				"and ["+maxBookCopies+"] maximum number of each book description.");
		
		ConnectionFactory cf = new ConnectionFactory(dbConfFileName);
		Connection conn = cf.createConnection();
		cf.closeConnection(conn);
		
		if ( conn == null)
			logger.error(
					"Couldn't establish a connection to the central" +
					" library database using configuration in ["+dbConfFileName+"].");
		dbw = new DatabaseWrapper(cf);

		books = BookFactory.createBooks(numBooks);
		logger.debug("Created ["+books.size()+"] books.");
		dbw.dropTable(Book.class);
		dbw.dropTable(BookDescription.class);
		dbw.createTable(Book.class);
		dbw.createTable(BookDescription.class);
		dbw.insertBeans(Book.class,books);
		logger.debug("Added ["+books.size()+"] books to database." );
		
		users = UserFactory.createUsersProfile(numUsers, probStaff);
		logger.debug("Created ["+users.size()+"] books.");

		dbw.dropTable(User.class);
		dbw.createTable(User.class);
		dbw.insertBeans(User.class, users);
		logger.debug("Added ["+users.size()+"] users to database." );		
	}


	/**
	 * @return user accounts used to initialise the database User table
	 */
	public List<User> getUsers() {
		return users;
	}

	/**
	 * @return the books (with references to descriptions) used to initialise the database
	 */
	public List<Book> getBooks() {
		return books;
	}
}