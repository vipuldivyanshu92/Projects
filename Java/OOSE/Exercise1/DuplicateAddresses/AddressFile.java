import java.io.InputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * Class representing an Address file
 * 
 * <p>Each Address file has an associated file name and a Scanner to that file
 * 
 * @author jsventek
 */
public class AddressFile {
	
	private String fileName;
	private Scanner scan;
	
	public AddressFile(String name) throws FileNotFoundException {
		this.fileName = name;
		InputStream s = new FileInputStream(new File(name));
		this.scan = new Scanner(s);
	}
	
	public AddressFile(InputStream s, String name) {
		this.fileName = name;
		this.scan = new Scanner(s);
	}
	
	public AddressFile(Scanner sc, String name) {
		this.fileName = name;
		this.scan = sc;
	}
	
	public Scanner getScanner() {
		return this.scan;
	}
	
	public String getFileName() {
		return this.fileName;
	}
}