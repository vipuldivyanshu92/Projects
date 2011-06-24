package uk.ac.gla.dcs.psd3.ay2009.project.model;

import java.io.Serializable;

public interface BookDescription extends Serializable{
	public abstract String getTitle();

	public abstract void setTitle(String title);

	public abstract String getAuthors();

	public abstract void setAuthors(String authors);

	public abstract String getPublished();

	public abstract void setPublished(String published);

	public abstract String getPublisher();

	public abstract void setPublisher(String publisher);

	public abstract String getISBN();

	public abstract void setISBN(String status);
	
	public abstract Integer getID();

	public abstract void setID(Integer id);
}
