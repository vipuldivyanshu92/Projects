import java.util.Scanner;
import java.io.PrintWriter;
import java.io.FileOutputStream;
import java.util.ArrayList;

public class GenTestLists {
	
	private static int i = 0;
	private static int j = 0;
	private static int k = 0;
	private static int l = 0;
	private static int m = 0;
	private static final String letters = "abcdefghijklmnopqrstuvwxyz";
	private static final String digits = "123456789";
		
	static public String genPostCode() {
		String pc = String.format("%c%c %c%c%c", letters.charAt(i), digits.charAt(j), digits.charAt(k), letters.charAt(l), letters.charAt(m));
		if (++m >= 26) {
			m = 0;
			if (++l >= 26) {
				l = 0;
				if (++k >= 9) {
					k = 0;
					if (++j >= 9) {
						j = 0;
						++i;
					}
				}
			}
		}
		return pc;
	}	

	public static void main(String[] args)
	{
		if (args.length != 2) {
			System.err.println("usage: GenTestLists no_of_unique_addresses no_of_addresses");
			System.exit(1);
		}
		Scanner sc = new Scanner(args[0]);
		int nunique = sc.nextInt();
		if (nunique > 26 * 26 * 26 * 9 * 9) {
			System.err.println("GenTestLists: Number of unique addresses may not exceed 26*26*26*9*9");
		}
		System.out.println("No of unique addresses is " + nunique);
		sc = new Scanner(args[1]);
		int ntotal = sc.nextInt();
		System.out.println("No of addresses is " + ntotal);
		if (ntotal < nunique) {
			System.err.println("GenTestLists: Number of addresses must be greater than or equal to number of unique addresses");
			System.exit(1);
		}
		int nduplicates = (ntotal - 1) / nunique + 1;
		System.out.println("No of duplicates per address is " + nduplicates);
		ArrayList<Address> al = new ArrayList<Address>(nunique);	// array list to hold unique addresses
		for (int i = 0; i < nunique; i++) {
			String s = String.format("Surname,F\n23 Skidoo Road, London\n%s\n", genPostCode());
			sc = new Scanner(s);
			AddressFile af = new AddressFile(sc, "name");
			Address a = null;
			try {
				a = Address.load(af);
			} catch (Exception e) {}
			al.add(a);
		}
		String filename = String.format("UA%dTA%d.dat", nunique, ntotal);
		PrintWriter out = null;
		try {
			out = new PrintWriter(new FileOutputStream(filename));
		} catch (Exception e) {
			System.err.println(e + "Cannot create the file " + filename);
			System.exit(1);
		}
		System.out.println("Created file " + filename);
		try {
			for (i = 0; i < nduplicates; i++) {
				for (int j = 0; j < nunique; j++) {
					Address a = al.get(j);
					a.print(out);
					if (--ntotal <= 0)
						throw new Exception("break out");
				}
			}
		} catch (Exception e) {
			// ignore exception, just used to break out of nested loops
		}
		out.close();
	}
}