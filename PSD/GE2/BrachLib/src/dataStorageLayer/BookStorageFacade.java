package dataStorageLayer;
import java.util.ArrayList;
import java.util.List;
import java.lang.String;

import applicationLayer.BranchBook;
import applicationLayer.BranchBookImpl;
import applicationLayer.Keeper;
import applicationLayer.States;

import uk.ac.gla.dcs.psd3.ay2009.project.CentralLibClient;
import uk.ac.gla.dcs.psd3.ay2009.project.CentralLibClientSQLImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.Book;

public class BookStorageFacade {
	private static BookStorageFacade instance = null;
	private CentralLibClient libClient = null;
	// *ToDo* Change this to the config file
	private static String dbPropertiesFN = "config/db.properties";
	
	private BookStorageFacade()	{
		libClient = new CentralLibClientSQLImpl(dbPropertiesFN);
	}
	
	public static BookStorageFacade getInstance() {
		if (instance == null)
			instance = new BookStorageFacade();
		
		return instance;
	}

	private BranchBook bookToBranchBook(Book b) throws Exception {
		BranchBook bb = new BranchBookImpl();
		
		// Load from Prolib data
		bb.setAuthors(b.getBookDescription().getAuthors());
		bb.setID(b.getID());
		bb.setISBN(b.getBookDescription().getISBN());
		bb.setPublished(b.getBookDescription().getPublished());
		bb.setPublisher(b.getBookDescription().getPublisher());
		bb.setTitle(b.getBookDescription().getTitle());
		
		// Load from local branch library database
		BranchStorageInterface bsi = BranchStorageInterface.getInstance();
		UserStorageFacade usf = UserStorageFacade.getInstance();
		
		try {
			bb.setState(bsi.getBookState(b.getID()));
		} catch (Exception e) {
			bb.setState(States.INCENTRAL);
		}
		try {
			bb.setKeeper((Keeper)usf.getUserById(bsi.getBookKeeper(b.getID())));
		} catch (Exception e) {
			bb.setKeeper(null);
		}
		try {
			bb.setBorrower(bb.getBorrower());
		} catch (Exception e) {
			bb.setBorrower(null);
		}
		
		return bb;
	}
	
	public BranchBook getBookByID(int id) throws Exception
	{
		/*	Return Branch Book by ID */
		return bookToBranchBook(libClient.getBookByID(id));
	}
	
	public List<BranchBook> getBooksBy(String key, Object value) throws Exception
	{
		List<BranchBook> bbl = new ArrayList<BranchBook>();
		if (key.equalsIgnoreCase("isbn"))
		{
			List<Book> bl = libClient.findBooksByDescription("ISBN='%" + value.toString() + "%'");
			for(Book b : bl) {
				bbl.add(bookToBranchBook(b));
			}
			//	Return book by ISBN
		} else if (key.equalsIgnoreCase("publisher")) {
			//	Return book by Publisher
			List<Book> bl = libClient.findBooksByDescription("Publisher='%" + value.toString() + "%'");
			for(Book b : bl) {
				bbl.add(bookToBranchBook(b));
			}
		} else if (key.equalsIgnoreCase("published")) {
			List<Book> bl = libClient.findBooksByDescription("Published='%" + value.toString() + "%'");
			for(Book b : bl) {
				bbl.add(bookToBranchBook(b));
			}
		} else if (key.equalsIgnoreCase("title")) {
			List<Book> bl = libClient.findBooksByDescription("Title='%" + value.toString() + "%'");
			for(Book b : bl) {
				bbl.add(bookToBranchBook(b));
			}
		} else if (key.equalsIgnoreCase("author")) {
			List<Book> bl = libClient.findBooksByDescription("Authors='%" + value.toString() + "%'");
			for(Book b : bl) {
				bbl.add(bookToBranchBook(b));
			}			
		} else if (key.equalsIgnoreCase("state")) {
			BranchStorageInterface bsi = BranchStorageInterface.getInstance();
			List<Integer> bl = bsi.getBooksByState((States)value);
			for(int b : bl) {
				bbl.add(getBookByID(b));
			}
		} else if (key.equalsIgnoreCase("borrower")) {
			BranchStorageInterface bsi = BranchStorageInterface.getInstance();
			List<Integer> bl = bsi.getBooksByBorrower((Integer)value);
			for(int b : bl) {
				bbl.add(getBookByID(b));
			}
		} else if (key.equalsIgnoreCase("keeper")) {
			BranchStorageInterface bsi = BranchStorageInterface.getInstance();
			List<Integer> bl = bsi.getBooksByKeeper((Integer)value);
			for(int b : bl) {
				bbl.add(getBookByID(b));
			}
		} else {
			throw new Exception("Unknown Key!");
		}
		return bbl;
	}
	
	public void setBookKeeper(int bookid, int userid) throws Exception {
		BranchStorageInterface bsi = BranchStorageInterface.getInstance();
		bsi.setBookKeeper(bookid, userid);
	}
	
	public int getBookBorrower(int bookid) throws Exception {
		BranchStorageInterface bsi = BranchStorageInterface.getInstance();
		return bsi.getBookKeeper(bookid);
	}
	
	public void setBookBorrower(int bookid, int userid) throws Exception {
		BranchStorageInterface bsi = BranchStorageInterface.getInstance();
		bsi.setBookBorrower(bookid, userid);
	}
	
	public void setBookState(int bookid, States s) throws Exception {
		BranchStorageInterface bsi = BranchStorageInterface.getInstance();
		bsi.setBookState(bookid, s);
	}
}
