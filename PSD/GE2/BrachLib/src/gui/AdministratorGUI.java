package gui;

public class AdministratorGUI extends KeeperGUI{

	private static final long serialVersionUID = 1L;

	public AdministratorGUI(String name){
		super(name);
		initGUI(name);
		this.setVisible(true);
	}
	
	private void initGUI(String s){
		addKeeperButton.setVisible(true);
		removeKeeperButton.setVisible(true);
	}
}
