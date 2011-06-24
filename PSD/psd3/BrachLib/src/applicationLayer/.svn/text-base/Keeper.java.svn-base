package applicationLayer;

import java.util.List;

import dataStorageLayer.BookStorageFacade;

class Keeper extends Borrower{
	
	public List<Book> getBooksResponsibleFor() throws Exception{
		
		List<Book>  bookList = BookStorageFacade.getBooksByKeeper(this.getId());
		
		return bookList;
	}

}
