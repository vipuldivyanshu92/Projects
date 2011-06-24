package gui;

import applicationLayer.BranchUser;
import applicationLayer.Privilege;

public class GUIFactory {

	private GUIFactory(){}
	
	/*todo change this to User not MainFrame*/
	public static UserGUI createGUI(BranchUser user) throws Exception{
		if(user.getPrivilege().equals(Privilege.KEEPER))
			return new KeeperGUI(user.getFirstName() + " "+ user.getLastName());
		else if(user.getPrivilege().equals(Privilege.ADMINISTRATOR))
			return new AdministratorGUI(user.getFirstName() + " "+ user.getLastName());
		else if (user.getPrivilege().equals(Privilege.BORROWER))
			return new BorrowerGUI(user.getFirstName() + " "+ user.getLastName());
		else
			throw new Exception("Privilege Unknown !");
		
	}
}
