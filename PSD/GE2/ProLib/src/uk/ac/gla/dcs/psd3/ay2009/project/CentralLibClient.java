package uk.ac.gla.dcs.psd3.ay2009.project;

import java.util.List;

import uk.ac.gla.dcs.psd3.ay2009.project.model.Book;
import uk.ac.gla.dcs.psd3.ay2009.project.model.Book.Status;
import uk.ac.gla.dcs.psd3.ay2009.project.model.User;

/**
 * A number of methods in CentralLibClient support queries over Java bean properties.
 * Queries are represented as String arguments. A bean query is a logical
 * expression over atomic beans. Beans are represented as : separated lists of
 * field=value pairs. Values are regular expressions in the SQL flavour.
 * 
 * @author tws
 * 
 */
public interface CentralLibClient {
	/**
	 * Searches for books with a description matching the specified query in 
	 * the database.
	 * 
	 * @param query
	 *            A string representation of a bean query over the properties in
	 *            BookDescription.
	 * @return a list of matching books.
	 */
	public abstract List<Book> findBooksByDescription(String query);

	/**
	 * Searches for user matching the specified query in the database.
	 * @param query A string representation of a bean query over the properties in User.
	 * @return
	 */
	public abstract List<User> findUsers(String query);

	/**
	 * Returns the singleton bean representing the Book with the specified ID,
	 * or null if no such book exists.
	 * @param ID
	 * @return a Book bean instance with the specified ID,
	 * or null if not book exists.
	 */
	public abstract Book getBookByID(Integer ID);

	/**
	 * Returns the singleton bean representing the User with the specified ID,
	 * or null if no such user exists.
	 * @param ID
	 * @return a User bean instance with the specified ID,
	 * or null if not user exists.
	 */
	public abstract User getUserByID(Integer ID);
	
	/**
	 * Sets the status of the book (specified by ID) to the specified value.
	 * 
	 * @param ID
	 *            the unique identifier for the book.
	 * @param status
	 *            the Status to set. By default, a books status is "IN_LIBRARY".
	 */
	public abstract void setStatus(Integer ID, Status status);


}