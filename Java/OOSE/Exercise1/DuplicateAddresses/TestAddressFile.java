import java.util.Scanner;

/**
 * Test harness for testing the AddressFile class
 * 
 * <p> tests out all three constructors, with a real filename and with a non-existent filename
 * <p> tests getFileName()
 * <p> tests getScanner()
 * 
 * @author jsventek
 *
 */
public class TestAddressFile {
	
	public static void main(String args[]) {
		AddressFile af1 = null;
		AddressFile af2 = null;
		AddressFile af3 = null;
		String s = null;
		
		try {
			af1 = new AddressFile("TestAddressList.dat");
		} catch (Exception e) {
			System.err.println("TestAddressFile: unable to open file that exists - TestAddress.dat");
			System.exit(1);
		}
		try {
			af2 = new AddressFile("FileThatDoesNotExist.dat");
		} catch (Exception e) {
			// do nothing, as the constructor should have raised an exception
		}
		af3 = new AddressFile(System.in, "Name for Standard Input");
		Scanner sc = new Scanner("Surname,F\n23 Skidoo Road, London\nA1 1AA\n");
		af2 = new AddressFile(sc, "Name for Scanner");
		s = af1.getFileName();
		if (! s.equals("TestAddressList.dat")) {
			System.err.println("TestAddressFile: Filename returned not identical to that used in constructor");
			System.err.println("TestAddressFile: Returned " + s + ", should have been 'TestAddressList.dat'");
			System.exit(1);
		}
		s = af2.getFileName();
		if (! s.equals("Name for Scanner")) {
			System.err.println("TestAddressFile: Filename returned not identical to that used in constructor");
			System.err.println("TestAddressFile: Returned " + s + ", should have been 'Name for Scanner'");
			System.exit(1);
		}
		s = af3.getFileName();
		if (! s.equals("Name for Standard Input")) {
			System.err.println("TestAddressFile: Filename returned not identical to that used in constructor");
			System.err.println("TestAddressFile: Returned " + s + ", should have been 'Name for Standard Input'");
			System.exit(1);
		}
		sc = af1.getScanner();
		sc = af2.getScanner();
		sc = af3.getScanner();
		System.out.println("TestAddressFile: All tests successfully executed");
	}
}