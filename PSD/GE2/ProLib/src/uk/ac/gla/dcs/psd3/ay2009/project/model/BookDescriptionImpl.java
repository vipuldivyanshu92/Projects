package uk.ac.gla.dcs.psd3.ay2009.project.model;

import java.io.Serializable;

@SuppressWarnings("serial")
public class BookDescriptionImpl implements BookDescription, Serializable {

	private String title;
	private String authors;
	private String published;
	private String publisher;
	private String ISBN;
	private Integer ID;
	
	public BookDescriptionImpl(
			String title,
			String authors,
			String published,
			String publisher,
			String ISBN,
			Integer ID
			) {
		super();
		this.title = title;
		this.authors = authors;
		this.published = published;
		this.publisher = publisher;
		this.ISBN = ISBN;
		this.ID = ID;
	}
	
	public BookDescriptionImpl() {
		super();
	}

	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#getTitle()
	 */
	public String getTitle() {
		return title;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#setTitle(java.lang.String)
	 */
	public void setTitle(String title) {
		this.title = title;
	}

	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#getAuthors()
	 */
	public String getAuthors() {
		return authors;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#setAuthors(java.lang.String)
	 */
	public void setAuthors(String authors) {
		this.authors = authors;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#getPublished()
	 */
	public String getPublished() {
		return published;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#setPublished(java.lang.String)
	 */
	public void setPublished(String published) {
		this.published = published;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#getPublisher()
	 */
	public String getPublisher() {
		return publisher;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#setPublisher(java.lang.String)
	 */
	public void setPublisher(String publisher) {
		this.publisher = publisher;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#getISBN()
	 */
	public String getISBN() {
		return ISBN;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#setISBN(java.lang.String)
	 */
	public void setISBN(String ISBN) {
		this.ISBN = ISBN;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#getID()
	 */
	public Integer getID() {
		return ID;
	}
	/* (non-Javadoc)
	 * @see uk.ac.gla.dcs.psd3.ay2009.project.BookDescription#setID(java.lang.Integer)
	 */
	public void setID(Integer ID) {
		this.ID = ID;	
	}
	
	@Override
	public String toString() {
		return "[ :\n" +
					" -title:     ["+title+"],\n" +
					" -authors:   ["+authors+"],\n" +
					" -published: ["+published+"],\n" +
					" -publisher: ["+publisher+"],\n" +
					" -ISBN: ["+ISBN+"]\n" +
					" -ID: ["+ID+"]\n" +
					"]";
	}
}
