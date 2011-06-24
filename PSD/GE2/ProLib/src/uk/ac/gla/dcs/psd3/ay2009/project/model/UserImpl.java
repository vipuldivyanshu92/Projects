package uk.ac.gla.dcs.psd3.ay2009.project.model;

import java.io.Serializable;

@SuppressWarnings("serial")
public class UserImpl implements User, Serializable {

	private String forename;
	private Integer ID;
	private String surname;
	private Boolean isStaff;
	
	/**
	 * @param iD
	 * @param surname
	 * @param forename
	 * @param isStaff
	 */
	public UserImpl(Integer iD, String surname, String forename, boolean isStaff) {
		super();
		ID = iD;
		this.surname = surname;
		this.forename = forename;
		this.isStaff = isStaff;
	}

	
	public UserImpl() {}

	@Override
	public String getForename() {
		return forename;
	}

	@Override
	public Integer getID() {
		return ID;
	}

	@Override
	public String getSurname() {
		return surname;
	}

	@Override
	public Boolean getIsStaff() {
		return isStaff;
	}
	
	@Override
	public void setIsStaff(Boolean isStaff) {
		this.isStaff = isStaff;
	}


	@Override
	public void setForename(String forename) {
		this.forename = forename;
	}

	@Override
	public void setID(Integer ID) {
		this.ID = ID;

	}

	@Override
	public void setSurname(String surname) {
		this.surname = surname;
	}

}
