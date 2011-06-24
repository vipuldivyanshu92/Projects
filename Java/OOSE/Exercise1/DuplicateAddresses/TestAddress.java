import java.io.PrintWriter;
import java.util.Scanner;

/**
 * Test harness for the Address class
 * <p>Tests all of the public methods defined for the Address class
 * <p>Tests to be sure that truncated addresses generate an exception
 * 
 * @author jsventek
 *
 */
public class TestAddress {

	private static Address fetchAddress(String s, String name) {
		Scanner sc = new Scanner(s);
		AddressFile af = new AddressFile(sc, name);
		Address a = null;
		try {
			a = Address.load(af);
		} catch (TruncatedAddressException e) {
			System.err.println("TestAddress: caught truncated address exception");
			System.exit(1);
		}
		if (a == null) {
			System.err.println("TestAddress: unable to load legal address");
			System.exit(1);
		}
		return a;
	}
	
	public static void main(String args[]) {
		PrintWriter out = new PrintWriter(System.out);
		String s1 = new String("surname, first\n1 main street, london\nn1 1zz\n");
		Address a1 = fetchAddress(s1, "name1");
		out.println("TestAddress: success - scanned a legal address");
		Address a2 = fetchAddress(s1, "name2");
		out.println("TestAddress: success - scanned the same legal address");
		if (a1.compareTo(a2) != 0) {
			System.err.println("TestAddress: identical addresses do not compare equal");
			System.exit(1);
		}
		out.println("TestAddress: success - compareTo() of identical addresses yields 0");
		String s2 = new String("aname, first\n1 main street, london\nn1 1zz\n");
		String s4 = new String("aname, first\n1 main street, london\nn11zz\n");
		a2 = fetchAddress(s2, "name3");
		Address a4 = fetchAddress(s4, "name4");
		if (a2.compareTo(a4) == 0) {
			out.println("TestAddress: success - compareTo() of differently formatted postcode yields 0");
		}
		out.println("TestAddress: success - scanned another address for which compareTo() should be >0");
		if (a1.compareTo(a2) <= 0) {
			System.err.println("TestAddress: 'surname+n1 1zz' should be > 'aname+n1 1zz'");
			System.exit(1);
		}
		out.println("TestAddress: success - compareTo() yielded a value >0");
		out.println("TestAddress: testing the print() methods");
		out.println("TestAddress: next address is unique");
		a1.print(out);
		out.println("TestAddress: next address is duplicate");
		a2.printAsDuplicate(out);
		out.println("TestAddress: testing scan of truncated address");
		String s3 = new String("bname, first\n");
		Scanner sc3 = new Scanner(s3);
		AddressFile af3 = new AddressFile(sc3, "yet another name");
		try {
			a2 =Address.load(af3);
		} catch (TruncatedAddressException e) {
			out.println("TestAddress: success - caught truncated address exception");
		}
		out.println("TestAddress: all tests executed successfully");
		out.flush();
		out.close();
	}
}
