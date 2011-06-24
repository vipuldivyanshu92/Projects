import java.io.PrintWriter;
/**
 * Interface supported by all implementations of AddressList
 * 
 * @author jsventek
 *
 */
public interface AddressListIF {
	/**
	 * add an Address instance to the AddressList
	 * 
	 * <p>if it does not match any of the existing addresses in the list, it is added to the list
	 * 
	 * <p>if it matches an entry already in the list, it is added to the duplicates list associated with that entry
	 * 
	 * @param a Address instance to add to the AddressList
	 */
	public void add(Address a);
	
	/**
	 * print the AddressList to 'out'
	 * 
	 * <p>it prints out each entry; if that entry has any duplicates, it then prints out the duplicates as commented lines
	 * 
	 * @param out a PrintWriter onto file "MergedAddresses.out"
	 */
	public void print(PrintWriter out);
	
	/**
	 * return the number of unique addresses in the AddressList
	 * 
	 * @return the current number of unique addresses in this
	 */
	public int size();
}