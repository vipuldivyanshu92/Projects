import javax.net.ssl.SSLServerSocketFactory;
import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.SSLSocket;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class SSLServer {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try {
			SSLServerSocketFactory socketFactory = (SSLServerSocketFactory)SSLServerSocketFactory.getDefault();
			SSLServerSocket sslserversocket = (SSLServerSocket)socketFactory.createServerSocket(443);
			SSLSocket sslsocket = (SSLSocket)sslserversocket.accept();
			
			// Enumeration of the SSL Ciphers
			System.out.println("*** Enumeration of SSL ciphers");
			for(String s : sslsocket.getEnabledCipherSuites()) {
				System.out.println(s);
			}
			System.out.println("*** End of enumeration\n");
			// End enumeration
			
			// Enumeration of the SSL protocols
			System.out.println("*** Enumeration of SSL protocols");
			for(String s : sslsocket.getEnabledProtocols()) {
				System.out.println(s);
			}
			System.out.println("*** End of enumeration\n");
			// End enumeration
			
			System.out.println(sslsocket.getSession().getCipherSuite());
			
	        InputStream inputstream = sslsocket.getInputStream();
	        InputStreamReader inputstreamreader = new InputStreamReader(inputstream);
	        BufferedReader bufferedreader = new BufferedReader(inputstreamreader);
	        
	        String string = null;
            while ((string = bufferedreader.readLine()) != null) {
                System.out.println(string);
                System.out.flush();
            }

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
