import java.util.ArrayList;
import java.io.PrintWriter;

/**
 * Class that implements an AddressList - list of unique address is maintained as an ArrayList of Address instances
 * 
 * <p>Each Address instance has a reference to an ArrayList of Address instances that are potential duplicates
 * 
 * @author jsventek
 */
public class AddressList implements AddressListIF {
	
	private ArrayList<Address> theList;
	
	public AddressList() {
		theList = new ArrayList<Address>();
	}
	
	/**
	 * implementation of the AddressListIF.add() method
	 * 
	 * @param a Address instance to add to the AddressList
	 */
	public void add(Address a) {
		int left, right, mid = 0, n;
		Address temp = null;
		n = theList.size();
		
		// Empty list, just add and return
		if (n == 0) {
			theList.add(a);
			return;
		}
		
		left = 0;
		right = n - 1;
		temp = theList.get(left);
		
		// less than leftmost, insert there
		if (a.compareTo(temp) < 0) {
			theList.add(left, a);
			return;
		}
		
		temp = theList.get(right);
		
		// greater than right, insert there
		if (a.compareTo(temp) > 0) {
			theList.add(n, a);
			return;
		}
		
		// first time through left < right
		while (left <= right) {
			mid = (left + right) / 2;
			temp = theList.get(mid);
			int cv = a.compareTo(temp);
			if (cv < 0)
				right = mid - 1;
			else if (cv > 0)
				left = mid + 1;
			else {
				// string already in list
				ArrayList<Address> dups = theList.get(left).getDuplicates();
				dups.add(a);
				return;
			}
		}
		theList.add(left, a);
	}
	
	/**
	 * implementation of the AddressListIF.print() method
	 * 
	 * @param out a PrintWriter onto file "MergedAddresses.out"
	 */
	public void print(PrintWriter out) {
		for (int i = 0; i < theList.size(); i++) {
			Address a = theList.get(i);
			a.print(out);
			ArrayList<Address> dups = a.getDuplicates();
			if (dups.size() != 0) {
				out.println("!Begin Potential Duplicates");
				for (int j = 0; j < dups.size(); j++) {
					Address b = dups.get(j);
					b.printAsDuplicate(out);
				}
				out.println("!End   Potential duplicates");
			}
		}
	}
	
	/**
	 * implementation of the AddressListIF.size() method
	 * 
	 * @return size of AddressList
	 */
	public int size() {
		return theList.size();
	}
}