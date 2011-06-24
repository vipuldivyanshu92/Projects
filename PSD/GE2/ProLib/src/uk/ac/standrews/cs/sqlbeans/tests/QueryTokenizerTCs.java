package uk.ac.standrews.cs.sqlbeans.tests;

import static org.junit.Assert.*;

import java.util.Queue;

import org.junit.Test;

import uk.ac.standrews.cs.sqlbeans.QueryTokenizer;

public class QueryTokenizerTCs {

	private String andOrQuery = "(Authors='Sommerville, I%' AND Title='Software%')";
	
	@Test
	public void testANDOR(){		
		Queue<String> tokens = QueryTokenizer.makeTokenStream(andOrQuery+"\n"); 
		assertEquals("(",tokens.poll());
		assertEquals("Authors",tokens.poll());
		assertEquals("=",tokens.poll());
		assertEquals("Sommerville, I%",tokens.poll());

		assertEquals("AND",tokens.poll());
		assertEquals("Title",tokens.poll());
		assertEquals("=",tokens.poll());
		assertEquals("Software%",tokens.poll());
		assertEquals(")",tokens.poll());
	}
	
	@Test
	public void testIntValue (){
		String query = "Title=\"Application and theory of petri nets" +
				" 1999 :20th International Conference, ICATPN'99," +
				" Williamsburg, Virginia, USA, June 21-25, 1999 : proceedings /\"";
		Queue<String> tokens = QueryTokenizer.makeTokenStream(query);
		assertEquals("Title",tokens.poll());
		assertEquals("=",tokens.poll());
		assertEquals("Application and theory of petri nets" +
				" 1999 :20th International Conference, ICATPN'99," +
				" Williamsburg, Virginia, USA, June 21-25, 1999 : proceedings /",tokens.poll());

	}
	
	@Test(timeout=1000)
	public void testNoEOL (){
		QueryTokenizer.makeTokenStream(andOrQuery); 
	}
}
