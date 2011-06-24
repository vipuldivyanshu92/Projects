package applicationLayer;

import java.util.List;
import dataStorageLayer.BookStorageFacade;

public class Keeper extends Borrower {
	
	public List<BranchBook> getBooksResponsibleFor() throws Exception{
		
		BookStorageFacade bsf = BookStorageFacade.getInstance();
		List<BranchBook> bookList = bsf.getBooksBy("keeper", this.getId());
		
		return bookList;
	}

}
