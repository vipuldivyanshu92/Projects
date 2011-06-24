import java.net.InetSocketAddress;
  
import org.apache.mina.core.future.ConnectFuture;
import org.apache.mina.transport.socket.nio.NioSocketConnector;
import org.apache.mina.filter.codec.ProtocolCodecFilter;

public class Main {

	public static void main(String[] args) {
		// Create TCP/IP connector.
		NioSocketConnector connector = new NioSocketConnector();
		
		// Set connect timeout.
		connector.setConnectTimeoutMillis(30*1000L);
		
		// Start communication.
        connector.getFilterChain().addLast("codec", new ProtocolCodecFilter(new WowCodecFactory()));
		connector.setHandler(new RealmProtocolHandler());
		ConnectFuture cf = connector.connect(
				new InetSocketAddress("91.121.148.199", 3724));
		
		// Wait for the connection attempt to be finished.
		cf.awaitUninterruptibly();
		cf.getSession().getCloseFuture().awaitUninterruptibly();
		connector.dispose();
	}

}
