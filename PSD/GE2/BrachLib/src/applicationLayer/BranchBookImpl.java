package applicationLayer;

/**
 * Team implementation of a branchbook
 */
public class BranchBookImpl implements BranchBook
{
	private int ID;
	private String title, authors, published, publisher, ISBN;
	States state;
	Borrower borrower;
	Keeper keeper;
	
	public int getID() {
		return ID;
	}
	
	public void setID(int id) {
		ID = id;
	}
	
	public String getTitle() {
		return title;
	}
	
	public void setTitle(String title) {
		this.title = title;
	}
	
	public String getAuthors() {
		return authors;
	}
	
	public void setAuthors(String authors) {
		this.authors = authors;
	}
	
	public String getPublished() {
		return published;
	}
	
	public void setPublished(String published) {
		this.published = published;
	}
	
	public String getPublisher() {
		return publisher;
	}
	
	public void setPublisher(String publisher) {
		this.publisher = publisher;
	}
	
	public String getISBN() {
		return ISBN;
	}
	
	public void setISBN(String isbn) {
		ISBN = isbn;
	}
	public States getState() {
		return state;
	}
	
	public void setState(States state) {
		this.state = state;
	}
	
	public Borrower getBorrower() {
		return borrower;
	}
	
	public void setBorrower(Borrower borrower) {
		this.borrower = borrower;
	}
	
	public Keeper getKeeper() {
		return keeper;
	}
	
	public void setKeeper(Keeper keeper) {
		this.keeper = keeper;
	}
}
