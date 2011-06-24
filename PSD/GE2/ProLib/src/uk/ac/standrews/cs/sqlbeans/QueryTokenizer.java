package uk.ac.standrews.cs.sqlbeans;

import java.io.IOException;
import java.io.StreamTokenizer;
import java.io.StringReader;
import java.util.LinkedList;
import java.util.Queue;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

public class QueryTokenizer {
	
	private static final Logger logger = 
		L4JConfiguredLoggerFactory.getConfiguredL4JLogger(QueryTokenizer.class);
	
	public static final String WS = " ";
	
	public static Queue<String> makeTokenStream(String query){
		Queue<String> list = new LinkedList<String>();
				
		StreamTokenizer st = new StreamTokenizer(new StringReader(query));
		st.quoteChar('\'');
		st.quoteChar('\"');
		st.eolIsSignificant(true);	
		st.wordChars('0', '9');
		try {
			int tok = st.nextToken();
			
			while (tok != StreamTokenizer.TT_EOL && tok != StreamTokenizer.TT_EOF){

				switch(tok){
					case StreamTokenizer.TT_WORD : list.offer(st.sval); break;
					case '\'' :
					case '\"' : list.offer(st.sval); break;
					//case StreamTokenizer.TT_NUMBER:
					//	list.offer(""+st.nval);break;
					default   : list.offer(Character.toString((char)tok)); break;
				}
				
				tok = st.nextToken();
			}
		} catch (IOException e) {
			logger.error("While tokenizing query string ["+query+"].",e);
		}	
		return list;
	}
}
