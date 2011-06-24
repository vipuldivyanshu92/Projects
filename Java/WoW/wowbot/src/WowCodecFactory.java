import org.apache.mina.core.session.IoSession;
import org.apache.mina.filter.codec.ProtocolCodecFactory;
import org.apache.mina.filter.codec.ProtocolEncoder;
import org.apache.mina.filter.codec.ProtocolDecoder;


public class WowCodecFactory implements ProtocolCodecFactory {
	private ProtocolEncoder encoder = new WowRequestEncoder();
	private ProtocolDecoder decoder = new WowResponseEncoder();

	public ProtocolEncoder getEncoder(IoSession ioSession) throws Exception {
		return encoder;
	}
	
	public ProtocolDecoder getDecoder(IoSession ioSession) throws Exception {
		return decoder;
	}
}
