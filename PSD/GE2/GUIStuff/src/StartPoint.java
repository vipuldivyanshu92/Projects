
import java.awt.LayoutManager;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;


public class StartPoint extends JFrame{

	public static void main(String[] args) {
		new StartPoint();
	}
	
	StartPoint() {
		JLabel jlbHelloWorld = new JLabel("Weldome to thte branch Liobrary system");
		JPanel pl = new JPanel();
		pl.setLayout();
		this.getContentPane().add(pl);
		setTitle("Branch Library Sytem");
		add(jlbHelloWorld);
		this.setSize(100, 100);
		setVisible(true);
	}

}
