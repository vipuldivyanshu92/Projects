import java.util.ArrayList;
import java.io.FileNotFoundException;

/**
 * Auxiliary program for OOSE2 Assessed Exercise 1
 * 
 * <p>This program reads from one or more files and stores the unique addresses seen.  Duplicates
 * (that have the same surname and postcode) are stored as such with the unique address that they match.
 * 
 * The start time and end time for processing the AddressFile[s] is noted.  The total number of addresses
 * encountered, the number of unique addresses seen, and the elapsed time are printed on System,out.
 * 
 * @author jsventek
 */
public class TimedFind {

	/**
	 * 	
	 * @param args the names of address list files to be processed; if none are provided, addresses are read from
	 * System.in
	 */
	public static void main(String args[]) {
		AddressFile tempAdFile = null;
		ArrayList<AddressFile> adrFiles = new ArrayList<AddressFile>();	// an array list to hold the AddressFile's
		AddressListIF al = new AddressList();							// an AddressList
		int i = 0;
		
		if (args.length == 0) {
			tempAdFile = new AddressFile(System.in, "Standard Input");
			adrFiles.add(tempAdFile);
		} else {
			try {
				for (i = 0; i < args.length; i++) {
					tempAdFile = new AddressFile(args[i]);
					adrFiles.add(tempAdFile);
				}
			} catch (FileNotFoundException e) {
				System.err.println("Unable to find file named '" + args[i] + "'");
				System.exit(1);
			}
		}
		int numberOfAddresses = 0;
		long startTime = System.currentTimeMillis();
		for (i = 0; i < adrFiles.size(); i++) {					// for each address file
			tempAdFile = adrFiles.get(i);
			Address a = null;
			while (true) {										// collect each address in the file
				try {
					if ((a = Address.load(tempAdFile)) == null)
						break;
					al.add(a);
					numberOfAddresses++;
				} catch (TruncatedAddressException e) {
					System.err.println(tempAdFile.getFileName() + " - incomplete last address");
					System.exit(1);
				}
			}
		}
		long elapsedTime = System.currentTimeMillis() - startTime;
		System.out.println(String.format(
				"Total: %d, Unique: %d, Elapsed time: %d.%03d seconds",
				numberOfAddresses, al.size(), elapsedTime/1000, elapsedTime%1000));

	}
}