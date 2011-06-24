package uk.ac.gla.dcs.psd3.ay2009.project.model;

public interface Book {
	
	enum Status {IN_LIBRARY,IN_BRANCH};
	
	public abstract BookDescription getBookDescription();
	
	public abstract void setBookDescription(BookDescription description);
	
	public abstract Integer getID();
	
	public abstract void setID(Integer ID);
	
	public abstract Status getStatus();

	public abstract void setStatus(Status status);
}