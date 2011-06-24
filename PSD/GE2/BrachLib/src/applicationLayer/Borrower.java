package applicationLayer;

import java.util.List;
import dataStorageLayer.BookStorageFacade;

/**
 * Borrower is a user with the right to borrow books.
 */
public class Borrower extends BranchUserImpl {

	/**
	 * return a list of the books borrowed by this user.
	 * @return a list of branchBook
	 * @throws Exception
	 */
	public List<BranchBook> getBooksBorrowed() throws Exception{
		
		List<BranchBook> b;
		BookStorageFacade bsf = BookStorageFacade.getInstance();
		
		b = bsf.getBooksBy("borrower", this.getId());		
		return b; 
	}
	
}
