package uk.ac.gla.dcs.psd3.ay2009.project.model;

import java.io.Serializable;

public interface User extends Serializable {
	public Boolean getIsStaff();

	public void setIsStaff(Boolean isStaff);
	
	public String getSurname();
	
	public void setSurname(String surname);
		
	public String getForename();
	
	public void setForename(String forename);
	
	public Integer getID();
	
	public void setID(Integer id);
}
