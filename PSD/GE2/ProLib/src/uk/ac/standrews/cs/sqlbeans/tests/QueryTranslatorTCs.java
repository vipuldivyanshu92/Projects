package uk.ac.standrews.cs.sqlbeans.tests;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;

import uk.ac.standrews.cs.sqlbeans.QueryTranslator;


public class QueryTranslatorTCs {

	private QueryTranslator<TestBean> qt;
	
	@Before
	public void setUp(){
		qt = new QueryTranslator<TestBean>(TestBean.class);
	}
	
	@Test
	public void testANDOR(){
		String result = qt.resolveQuery("(Authors=\"Sommerville, I%\" AND Title=\"Software%\")\n").toSQLFormat();
		String expected = " ( Title LIKE \'Software%\' ) AND  ( TRUE  )  AND  ( Authors LIKE \'Sommerville, I%\' ) AND  ( TRUE  ) ";
		

		
		assertEquals (expected,result);
	}
	
	@Test
	public void testIntegerValue(){
		String result = qt.resolveQuery("(Authors=\"Sommerville, I%\" AND Published=\"1986\")\n").toSQLFormat();
		String expected = " ( Published LIKE \'1986\' ) AND  ( TRUE  )  AND  ( Authors LIKE \'Sommerville, I%\' ) AND  ( TRUE  ) ";
		assertEquals (expected,result);
	}
}
