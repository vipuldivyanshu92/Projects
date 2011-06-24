public class Prog12 {
	public static void main(String[] args) {		
		int i = 0;
		for (int k=0 ; k<128 ; k++) {
			i = k*k + 17;
		}
		System.out.println(" i : " + i);
		String str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		StringBuffer buffer = new StringBuffer();
		for (int k = 0;k<str.length()/3;k++) {
			buffer.append(str.substring(k+2,k+3));
		}
		System.out.println("Resultat : " + buffer.length());
	}
}