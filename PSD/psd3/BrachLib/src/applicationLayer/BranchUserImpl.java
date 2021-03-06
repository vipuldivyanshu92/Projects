package applicationLayer;

public class BranchUserImpl implements BranchUser {

	private int id;
	private Privilege privilege;
	private String firstName;
	private String lastName;
	private boolean isStaff;
	
		
	public Privilege getPrivilege(){
		return privilege;
	}
	
	public String getFirstName(){
		return firstName;
	}
	
	public String getLastName(){
		return lastName;
	}
	
	public int getId(){
		return id;
	}
	
	public void setFirstName(String fn) {
		firstName = fn;
	}
	
	public void setLastName(String ln) {
		lastName = ln;
	}

	public boolean getIsStaff() {
		return isStaff;
	}

	public void setId(int id) {
		this.id = id;
	}

	public void setIsStaff(boolean v) {
		isStaff = v;		
	}

	public void setPrivilege(Privilege p) {
		privilege = p;		
	}
}
