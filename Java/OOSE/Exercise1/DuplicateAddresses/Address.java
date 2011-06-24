import java.util.Scanner;
import java.util.ArrayList;
import java.io.PrintWriter;

/**
 * Implementation of the Class that represents a postal address
 * 
 * <p>No public constructors are defined for this class; instead, a user must invoke the
 * static function Address.load(AddressFile af) to obtain the next Address from file 'af'
 * 
 * @author jsventek
 *
 */
public class Address implements Comparable<Address> {
	
	private String line1;
	private String line2;
	private String line3;
	private String surname;
	private String postcode;
	private String fileName;
	private ArrayList<Address> duplicates;
	
	private Address() { // default constructor cannot be invoked publicly
		line1 = null; line2 = null; line3 = null;
		surname = null; postcode = null;
		fileName = null;
		duplicates = new ArrayList<Address>();
	}
	
	/**
	 * Static function that returns the next Address from an AddressFile
	 * 
	 * <p>This method skips all commented lines (those that start with "!", and checks for incomplete addresses
	 * at the end of an Address File
	 * 
	 * @param af address file to read for an Address
	 * @return the next address from the file or null if at end of file
	 */
	public static Address load(AddressFile af) throws TruncatedAddressException {
		Address a = new Address();
		Scanner s = af.getScanner();
		String b = null;
		
		a.fileName = af.getFileName();
		int i;
		for (i = 0; i < 3 && s.hasNext(); i++) {
			b = s.nextLine();
			if (b.charAt(0) == '!') {
				i--;
				continue;
			}
			switch (i) {
			case 0: a.line1 = new String(b); break;
			case 1: a.line2 = new String(b); break;
			case 2: a.line3 = new String(b); break;
			default: System.err.println("Internal error in Address.load()"); System.exit(1); break;
			}
		}
		if (i != 3) {
			if (i != 0)
				throw new TruncatedAddressException();	// incomplete address
			return null;								// last returned address exhausted the scanner
		}
		a.postcode = normalizePostCode(a.line3);
		Scanner ss = new Scanner(a.line1);
		ss.useDelimiter(",");
		b = ss.next();
		a.surname = b;
		return a;
	}
	
	/**
	 * Return a postCode without any leading and trailing black chars. and
	 * remove any inner spaces.
	 * 
	 * @param pc is a postCode in a multitude of format.
	 * @return a String
	 */
	private static String normalizePostCode(String pc) {
		pc = pc.trim();
		pc = pc.replace(" ", "");
		return pc.toUpperCase();
	}

	/**
	 * Implementation of compareTo()
	 * 
	 * <p>Returns <0, 0, >0 if this < a, this == a, or this >a, respectively
	 * 
	 * <p>Depends upon String.compareTo()
	 * 
	 * @param a the Address against which to compare
	 * @return <0|0|>0 as described above
	 */
	public int compareTo(Address a) {
		int result;
		
		if ((result = this.surname.compareToIgnoreCase(a.surname)) == 0)
			result = this.postcode.compareTo(a.postcode);
		return result;
	}
	
	/**
	 * print extra information(s) about an address
	 * 
	 * @param out PrintWrite onto which the informations are written
	 */
	public void printExtraInformations(PrintWriter out) {
		// Print the fileName
		out.println("!FileName: " + this.fileName);
	}
	
	/**
	 * print this address onto out
	 * 
	 * @param out PrintWriter onto which the address is written
	 */
	public void print(PrintWriter out) {
		printExtraInformations(out);
		out.println(this.line1);
		out.println(this.line2);
		out.println(this.line3);
	}
	
	/**
	 * print this address prefixed by comment indicators on out
	 * 
	 * @param out PrintWriter onto which the address is written
	 */
	public void printAsDuplicate(PrintWriter out) {
		printExtraInformations(out);
		out.println("! " + this.line1);
		out.println("! " + this.line2);
		out.println("! " + this.line3);
	}
	
	/**
	 * return the ArrayList in which duplicates are kept
	 * 
	 * @return the ArrayList in which duplicates are kept
	 */
	public ArrayList<Address> getDuplicates() {
		return this.duplicates;
	}
}