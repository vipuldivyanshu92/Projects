package uk.ac.gla.dcs.psd3.ay2009.project.tests;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.util.List;
import java.util.Random;

import junit.framework.Assert;

import org.apache.log4j.Logger;
import org.junit.BeforeClass;
import org.junit.Test;

import uk.ac.gla.dcs.psd3.ay2009.project.CentralLibClient;
import uk.ac.gla.dcs.psd3.ay2009.project.CentralLibClientImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.Book;
import uk.ac.gla.dcs.psd3.ay2009.project.model.User;
import uk.ac.gla.dcs.psd3.ay2009.project.model.Book.Status;
import uk.ac.gla.dcs.psd3.ay2009.project.setup.SetupDB;
import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

public class CentraliLibClientImplTest {

	private Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(CentralLibClientImpl.class);
	
	private static CentralLibClient control;
	private static SetupDB setupDB;
	private static Random r;
	
	//Test case run specific constants
	private static String dbPropertiesFN = "config/test/db.properties";
	private static int numUsers = 10;
	private static double probStaff = .1; 
	private static int numBooks = 100;
	
	@BeforeClass
	public static void setUp() throws Exception {
		control = new CentralLibClientImpl(dbPropertiesFN);
		setupDB = new SetupDB(dbPropertiesFN, numUsers, probStaff,numBooks);
		r = new Random();

		setupDB.initialiseDB();
	}
	
	@Test
	public final void testFindBooksByTitle(){
		//Find a random book title and make sure that at least one book with that title
		//is returned from a search.
		Integer ID = r.nextInt(setupDB.getBooks().size());
		Book book = setupDB.getBooks().get(ID);
		
		String title = book.getBookDescription().getTitle();
				
		List<Book> books = control.findBooksByDescription("Title=\'"+title+"\'");
		
		logger.info("Searching for book with title ["+title+"] in database.");
		
		assertTrue(books.size() >= 1);	
	}
	
	@Test
	public final void testFindAllBooksByDescription(){
		List<Book> books = control.findBooksByDescription("Title=\"%\"");
		assertEquals(setupDB.getBooks().size(), books.size());
	}
	
	@Test
	public final void findUsersBySurname(){
		//Find a random book title and make sure that at least one book with that title
		//is returned from a search.
		Integer ID = r.nextInt(setupDB.getUsers().size());
		User user = setupDB.getUsers().get(ID);
		
		String surname = user.getSurname();
				
		List<User> users = control.findUsers("Surname=\'"+surname+"\'");
		
		logger.info("Searching for book with title ["+surname+"] in database.");
		
		assertTrue(users.size() >= 1);	
	}

	@Test
	public final void testSetStatus() {
		Integer ID = r.nextInt(setupDB.getBooks().size());
		
		Book book1 = control.getBookByID(ID);
		Status pre = book1.getStatus();
			
		if (pre == Status.IN_LIBRARY)
			control.setStatus(ID, Status.IN_BRANCH);
		else 
			control.setStatus(ID,Status.IN_LIBRARY);
		
		Book book2 = control.getBookByID(ID);
		
		Assert.assertNotSame(book1.getStatus(),book2.getStatus());
	}
}
