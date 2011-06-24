import java.util.ArrayList;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.FileOutputStream;

/**
 * Main program for OOSE2 Assessed Exercise 1
 * 
 * <p>This program reads from one or more files, stores the unique addresses seen, and then prints them out
 * to 'MergedAddresses.out'.
 * 
 * <p>If duplicate addresses are found (have the same surname and postcode), the first one encountered is
 * printed as the unique address, and all of the potential duplicates are printed immediately below it
 * in comment lines (lines that start with "!"
 * 
 * @author jsventek
 */
public class FindDuplicates {

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
		PrintWriter out = null;
		try {
			out = new PrintWriter(new FileOutputStream("MergedAddresses.out"));
		} catch (Exception e) {
			System.err.println(e + "Cannot create the file MergedAddresses.out");
			System.exit(1);
		}
		for (i = 0; i < adrFiles.size(); i++) {					// for each address file
			tempAdFile = adrFiles.get(i);
			Address a = null;
			while (true) {							// repeat until an exception or null address
				try {
					if ((a = Address.load(tempAdFile)) == null)
						break;
					al.add(a);
				} catch (TruncatedAddressException e) {
					System.err.println(tempAdFile.getFileName() + ": last address incomplete");
					break;
				}
			}
		}
		al.print(out);
		out.close();
	}
}