package uk.ac.gla.dcs.psd3.ay2009.project.model;

public class BookImpl implements Book  {
	
	private Integer ID;
	private Status status;
	private BookDescription bookDescription;
	
	public BookImpl(
			Integer ID,
			Status status,
			BookDescription bookDescription
			) {
		super();
		this.ID = ID;
		this.status = status;
		this.bookDescription = bookDescription;
	}
	
	public BookImpl() {
		super();
	}

	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Book#getID()
	 */
	public Integer getID() {
		return ID;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Book#setID(java.lang.Integer)
	 */
	@Override
	public void setID(Integer ID) {
		this.ID = ID;
	}

	
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Book#getStatus()
	 */
	public Status getStatus() {
		return status;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.Book#setStatus(java.lang.String)
	 */
	public void setStatus(Status status) {
		this.status = status;
	}
	
	@Override
	public String toString() {
		return "[ :\n" +
					" -ID: ["+ID+"]\n" +
					" -status: ["+status+"]\n" +
					" -description: ["+bookDescription+"]"+
					"]";
	}

	@Override
	public BookDescription getBookDescription() {
		return bookDescription;
	}

	@Override
	public void setBookDescription(BookDescription bookDescription) {
		this.bookDescription = bookDescription;
	}
}