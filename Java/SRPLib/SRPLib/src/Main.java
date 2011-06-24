/**
 * @author Simon Jouet
 * 
 * description : This class provide an implementation for SRP6a
 * 
 * definitions (from ref.2 ) :
 * 		- N is a large safe prime, all arithmetic is done modulo N
 * 		- g is a generator modulo N
 * 		- k is a multiplier parameter, k = H(N, g)
 * 		- s is the user salt
 * 		- I is the username
 * 		- p is the Cleartest password
 * 		- H() is the one-way hash function
 * 		- u is a random scrambling parameter
 * 		- a, b are secret ephemral values
 * 		- A, B are public ephemeral values
 * 		- x is the private key derived from p and s
 * 		- v is the password verifier 
 * 
 * references :
 * 		- (1) http://srp.stanford.edu/demo/demo.html
 * 		- (2) http://srp.stanford.edu/design.html
 */

import java.math.BigInteger;

public class Main {
	public static String nzero(int n) {
		if (n < 1)
			return "";
		String t = nzero(n >> 1);
		if ((n & 1) == 0)
			return t + t;
		else
			return t + t + "0";
	}
	
	public static BigInteger srp_compute_k(BigInteger N, int g) {
		// Convert both N and h to hex strings
		String nhex = N.toString(16);
		String ghex = Integer.toString(g, 16);
		
		// String hashIn is the concatenation of two equals length strings
		// which represent n and h in hex, the length difference is padded
		// with zeros
		String hashIn;
		
		if ((nhex.length() & 1) == 0)
			hashIn = nhex;
		else
			hashIn = "0" + nhex;
		
		hashIn += nzero(nhex.length() - ghex.length());
		hashIn += ghex;
		
		SHA1 hashfunc = new SHA1();
		hashfunc.setHex(hashIn);
		BigInteger k = new BigInteger(hashfunc.getHexDigest(), 16);
		
		// k should be moduloed (?) by N if k is greater than N
		if (k.compareTo(N) < 0)
			return k;
		else
			return k.mod(N);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {		
		// Modulus (N), radix 16
		BigInteger N = new BigInteger("115b8b692e0e045692cf280b436735c77a5a9e8a9e7ed56c965f87db5b2a2ece3", 16);
		
		// Generator (g)
		int g = 2;
		
		// Multiplier (k), k = H(N, g)
		BigInteger k = srp_compute_k(N, g);
	}

}
