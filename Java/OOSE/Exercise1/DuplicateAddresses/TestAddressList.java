import java.io.PrintWriter;

/**
 * Test harness for the AddressList class
 * <p>Uses the data from TestAddress.dat to load an instance of an address list and to manipulate it
 * 
 * @author jsventek
 *
 */
public class TestAddressList {
	
	public static void main(String args[]) {
		AddressFile af1 = null;
		AddressListIF al = new AddressList();
		Address a = null;
		PrintWriter out = new PrintWriter(System.out);
		
		try {
			af1 = new AddressFile("TestAddressList.dat");
		} catch (Exception e) {
			System.err.println("TestAddressList: unable to open file that exists - TestAddressList.dat");
			System.exit(1);
		}
		out.println("TestAddressList: number of unique addresses before loading file: " + al.size());
		while (true) {						// fetch each address from the file
			try {
				if ((a = Address.load(af1)) == null)	// no more addresses
					break;
				al.add(a);
			} catch (TruncatedAddressException e) {
				System.err.println("TestAddressList: incomplete last address in TestAddressList.dat");
				System.exit(1);
			}
		}
		out.println("TestAddressList: number of unique addresses after loading file: " + al.size());
		out.println("TestAddressList: now invoking print() on the AddressList created from the file");
		al.print(out);
		out.println("TestAddressList: all tests successfully completed");
		out.flush();
		out.close();
	}
}