package uk.ac.standrews.cs.sqlbeans.tests;

public class TestBean {
	
	private String authors;
	private String title;
	private String published;
	
	public String getPublished() {
		return published;
	}

	public void setPublished(String published) {
		this.published = published;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public TestBean(){}
	
	public String getAuthors(){
		return authors;
	}
	
	public void setAuthors(String authors){
		this.authors = authors;
	}
}
