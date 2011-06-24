/**
 * @author Simon Jouet
 *
 * This class is just SHA implementation as http://srp.stanford.edu/demo/sha1.js
 * converted in java and object oriented.
 * 
 * All credits are due to Paul Johnston and Tom Wu
 */

public class SHA1 {
	/*
	 * Classe variables
	 */
	private int[] blks;
	private String hash;
	
	/*
	 * Bitwise rotate a 32-bit number to the left
	 */
	private static int rol(int num, int cnt)
	{
		return (num << cnt) | (num >>> (32 - cnt));
	}
	
	/*
	 * Add integers, wrapping at 2^32. This uses 16-bit operations internally.
	 */
	private static int add(int x, int y)
	{
		int lsw = (x & 0xFFFF) + (y & 0xFFFF);
		int msw = (x >> 16) + (y >> 16) + (lsw >> 16);
		return (msw << 16) | (lsw & 0xFFFF);
	}
	
	/*
	 * Perform the appropriate triplet combination function for the current
	 * iteration
	 */
	private static int ft(int t, int b, int c, int d)
	{
		if(t < 20) return (b & c) | ((~b) & d);
		if(t < 40) return b ^ c ^ d;
		if(t < 60) return (b & c) | (b & d) | (c & d);
		return b ^ c ^ d;
	}
	
	/*
	 * Determine the appropriate additive constant for the current iteration
	 */
	private static int kt(int t)
	{
		return (t < 20) ?  1518500249 : (t < 40) ?  1859775393 :
	         (t < 60) ? -1894007588 : -899497514;
	}
	
	/*
	 * Input is in hex format - trailing odd nibble gets a zero appended.
	 */
	private static int[] hex2blks(String hex) {
		int len = (hex.length() + 1) >> 1;
		int nblk = ((len + 8) >> 6) + 1;
		int[] blks = new int[nblk * 16];
		int i = 0;
		
		for (i = 0; i < nblk * 16; i++)
			blks[i] = 0;
		
		for (i = 0; i < len; i++) {
			String sub;
			if ((2*i + 2) < hex.length()) {
				sub = hex.substring(2*i, 2*i + 2);
			} else {
				sub = hex.substring(2*i);
			}
			blks[i >> 2] |= Integer.parseInt(sub, 16) << (24 - (i % 4) * 8);
		}
		
		blks[i >> 2] |= 0x80 << (24 - (i % 4) * 8);
		blks[nblk * 16 - 1] = len * 8;
		
		return blks;
	}
	
	/*
	 * Convert a string to a sequence of 16-word blocks, stored as an array.
	 * Append padding bits and the length, as described in the SHA1 standard.
	 */
	private static int[] str2blks(String str) {
		int nblk = ((str.length() + 8) >> 6) + 1;
		int[] blks = new int[nblk * 16];
		int i = 0;
		
		for (i = 0; i < nblk * 16; i++)
			blks[i] = 0;
		
		for (i = 0; i < str.length(); i++)
			blks[i >> 2] |= (int)str.charAt(i) << (24 - (i % 4) * 8);
		
		blks[i >> 2] |= 0x80 << (24 - (i % 4) * 8);
		blks[nblk * 16 - 1] = str.length() * 8;
		return blks;
	}
	
	/*
	 * Convert a byte array to 16-word blocks, stored as an array.
	 * Append padding bits and the length, as described in the SHA1 standard.
	 */
	private static int[] ba2blks(byte[] ba, int off, int len) {
		int nblk = ((len + 8) >> 6) + 1;
		int[] blks = new int[nblk * 16];
		int i = 0;
		
		for (i = 0; i < nblk * 16; i++)
			blks[i] = 0;
		
		for (i = 0; i < len; i++)
			blks[i >> 2] |= (ba[off + i] & 0xFF) << (24 - (i % 4) * 8);
		
		blks[i >> 2] |= 0x80 << (24 - (i % 4) * 8);
		blks[nblk * 16 - 1] = len * 8;
		return blks;
	}
	
	private static int[] calcSHA1Raw(int[] x) {
		int[] w = new int[80];
		
		int a =  1732584193;
		int b = -271733879;
		int c = -1732584194;
		int d =  271733878;
		int e = -1009589776;
		  
		for (int i = 0; i < x.length; i+=16) {
			int olda = a;
			int oldb = b;
			int oldc = c;
			int oldd = d;
			int olde = e;
			
			for (int j = 0; j < 80; j++) {
				int t;
				
				if (j < 16)
					w[j] = x[i + j];
				else
					w[j] = rol(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1);
				
			    t = add(add(rol(a, 5), ft(j, b, c, d)), add(add(e, w[j]), kt(j)));
			    e = d;
			    d = c;
			    c = rol(b, 30);
			    b = a;
			    a = t;
			}
			
		    a = add(a, olda);
		    b = add(b, oldb);
		    c = add(c, oldc);
		    d = add(d, oldd);
		    e = add(e, olde);
		}
		return new int[]{a, b, c, d, e};
	}

	/*
	 * Class external calls
	 */
	
	/**
	 * Hash the plain string in parameter
	 * @param str is a string to hash
	 */
	public void setString(String str) {
		blks = str2blks(str);
		hash = null;
	}
	
	/**
	 * Hash the hexadecimal value in parameter
	 * @param hex is an hexadecimal string to hash
	 */
	public void setHex(String hex) {
		blks = hex2blks(hex);
		hash = null;
	}
	
	/**
	 * Hash the byte array in parameter
	 * @param ba is a byte array to hash
	 */
	public void setByteArray(byte[] ba) {
		blks = ba2blks(ba, 0, ba.length);
		hash = null;
	}
	
	/**
	 * Hash the byte array with specified length and offset
	 * @param ba is the byte array
	 * @param off is the offset
	 * @param len is the length
	 */
	public void setByteArray(byte[] ba, int off, int len) {
		blks = ba2blks(ba, off, len);
		hash = null;
	}
	
	/**
	 * Get the hex digest of this SHA1 hash
	 * @return a string representing the hash in hex
	 */
	public String getHexDigest() {
		if (hash == null) {
			int[] s = calcSHA1Raw(blks);
			hash = "";
			for (int i : s)
				hash += Integer.toHexString(i);
		}
		
		return hash;
	}
	
	public String toString() {
		return getHexDigest();
	}
}
