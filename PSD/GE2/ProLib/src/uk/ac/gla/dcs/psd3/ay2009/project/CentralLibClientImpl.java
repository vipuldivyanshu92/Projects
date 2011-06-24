package uk.ac.gla.dcs.psd3.ay2009.project;

import java.sql.Connection;
import java.util.List;

import org.apache.log4j.Logger;

import uk.ac.gla.dcs.psd3.ay2009.project.model.Book;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookDescription;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookDescriptionImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.User;
import uk.ac.gla.dcs.psd3.ay2009.project.model.UserImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.Book.Status;
import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.standrews.cs.sqlbeans.DatabaseWrapper;
import uk.ac.standrews.cs.sqlbeans.QueryTranslator;
import uk.ac.standrews.cs.sqlbeans.factories.ConnectionFactory;
import uk.ac.standrews.cs.sqlbeans.query.BeanCondition;

public class CentralLibClientImpl implements CentralLibClient {
	
	private static final Logger logger =  L4JConfiguredLoggerFactory.getConfiguredL4JLogger(CentralLibClientImpl.class);
	private DatabaseWrapper dbw;
	
	/**
	 * Constructs a new control for the specified database.
	 * @param dbConfFileName
	 */
	public CentralLibClientImpl (String dbConfFileName){
		ConnectionFactory cf = new ConnectionFactory(dbConfFileName);
		Connection conn = cf.createConnection();
		
		if ( conn == null)
			logger.error(
					"Couldn't establish a connection to the central" +
					" library database using configuration in ["+dbConfFileName+"].");
		
		cf.closeConnection(conn);
		
		dbw = new DatabaseWrapper(cf);
	} 
	
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Control#findBooks(java.lang.String)
	 */
	@Override
	public List<Book> findBooksByDescription(String query) {
		logger.debug("Looking for books matching query ["+query+"].\n");
		List<Book> books = null;
		
		QueryTranslator<BookDescription> descQT = new QueryTranslator<BookDescription>(BookDescriptionImpl.class);
		BeanCondition<BookDescription> descriptionCondition = descQT.resolveQuery(query);
		
		if (descriptionCondition==null) return books;
		
		String sqlQuery = "SELECT Book.* FROM" +
				          " (Book INNER JOIN BookDescription ON Book.BookDescription=BookDescription.ID)" +
				          "  WHERE "+descriptionCondition.toSQLFormat();
		
		books = dbw.getEntitySet(sqlQuery, Book.class);
		logger.debug("Found books ["+books+"].\n");
		return books;
	}

	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Control#findUsers(java.lang.String)
	 */
	@Override
	public List<User> findUsers(String query) {
		logger.debug("Looking for users matching query ["+query+"].\n");
		List<User> users = null;
		
		QueryTranslator<User> usersQT = new QueryTranslator<User>(UserImpl.class);
		BeanCondition<User> usersCondition = usersQT.resolveQuery(query);
		
		users = dbw.getEntitySet(usersCondition, User.class);
		logger.debug("Found users ["+users+"].\n");
		return users;
	}

	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Control#getUserByID(java.lang.Integer)
	 */
	@Override
	public User getUserByID(Integer ID) {
		return dbw.getBeanByID(User.class, ID);
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Control#getBookByID(java.lang.Integer)
	 */
	@Override
	public Book getBookByID(Integer ID){
		return dbw.getBeanByID(Book.class, ID);
	}
	
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Control#setStatus(int, java.lang.String)
	 */
	@Override
 	public void setStatus(Integer ID, Status status){
 		Book book = new BookImpl();
		QueryTranslator<Book> qt = new QueryTranslator<Book>(BookImpl.class);
 		BeanCondition<Book> beanCondition = qt.resolveQuery("ID='"+ID+"'\n");
 		book.setStatus(status);
		dbw.updateBeans(Book.class, book, beanCondition);	
	}
}
