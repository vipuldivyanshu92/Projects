package uk.ac.standrews.cs.sqlbeans;

import java.util.HashMap;
import java.util.Queue;
import java.util.Stack;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;
import uk.ac.standrews.cs.sqlbeans.query.AndBeanCondition;
import uk.ac.standrews.cs.sqlbeans.query.AndBeanConditionImpl;
import uk.ac.standrews.cs.sqlbeans.query.AtomicBeanCondition;
import uk.ac.standrews.cs.sqlbeans.query.AtomicBeanConditionImpl;
import uk.ac.standrews.cs.sqlbeans.query.BeanCondition;
import uk.ac.standrews.cs.sqlbeans.query.FalseBeanConditionImpl;
import uk.ac.standrews.cs.sqlbeans.query.NotBeanConditionImpl;
import uk.ac.standrews.cs.sqlbeans.query.OrBeanCondition;
import uk.ac.standrews.cs.sqlbeans.query.OrBeanConditionImpl;
import uk.ac.standrews.cs.sqlbeans.util.BeanFactory;
import uk.ac.standrews.cs.sqlbeans.util.ReflectionUtil;

/**
 * A utility class for translating string representations of bean queries into
 * programmatic query structures.   Queries are logical formulas over atomic string
 * serialisations of beans. A bean serialisation is a : separated list of field=value
 * pairs.
 * @author tws
 *
 * @param <T> the target bean format.
 */
public class QueryTranslator <T>{
	
	private static final Logger logger = 
		L4JConfiguredLoggerFactory.getConfiguredL4JLogger(QueryTranslator.class);
	
	private Stack<BeanCondition<T>> values = new Stack<BeanCondition<T>>();
	private Stack<String> operators = new Stack<String>();
	
	
	public static final String OR = "OR";
	public static final String AND = "AND";
	public static final String NOT = "NOT";
	public static final String OB = "(";
	public static final String CB = ")";
	
	private static final String[] ordering = {NOT, AND, OR};
	
	private Class<? extends T> beanType;
	
	public QueryTranslator (Class<? extends T> beanType){
		this.beanType = beanType;
	}
		
	private AtomicBeanCondition<T> buildBeanFor(String field, String value){
		
		HashMap<String,Object> map = new HashMap<String,Object>();
		Class<?> proptype = ReflectionUtil.getPropertyType(beanType, field);
		Object val = parseStringValue(proptype, value);
		if (val!= null) map.put(field,val);				
		
		T bean = new BeanFactory().createNewBean(map,beanType);		
		return new AtomicBeanConditionImpl<T>(bean,beanType);
	}
	
	private static Object parseStringValue(Class<?> proptype, String value){
		if (proptype==String.class) return value;
		else if (proptype==Integer.class){
			try{
				return new Integer(value);	
			} catch(NumberFormatException nfe){
				logger.error(
						"While parsing value ["+
						value+
						"] with expected property type ["
						+proptype+
						"].");
				return null;
			}
		}
			
		else return null;
	}
	
	private AndBeanCondition<T> and (BeanCondition<T> l, BeanCondition<T> r){
		return new AndBeanConditionImpl<T>(l,r);
	}

	private OrBeanCondition<T> or (BeanCondition<T> l, BeanCondition<T> r){
		return new OrBeanConditionImpl<T>(l,r);
	}
	
	private BeanCondition<T> not (BeanCondition<T> r){
		return new NotBeanConditionImpl<T>(r);
	}
	
	private int getPrecedenceFor(String token){
		for (int i = 0; i < ordering.length;i++)
			if (token.equalsIgnoreCase(ordering[i])) return i;
		return ordering.length+1;
	}
	
	private boolean isHigherPrecedence(String token1, String token2){
		return getPrecedenceFor(token1) < getPrecedenceFor(token2);
	}
	
	private void doOperationFor(String token){
		if (token.equalsIgnoreCase(NOT)) values.push(not(values.pop()));
		else if (token.equalsIgnoreCase(AND))  values.push(and(values.pop(),values.pop()));
		else if (token.equals(OR))values.push(or(values.pop(),values.pop()));
	}
	
	private boolean isOperator(String token){
		for (String operator: ordering)
			if (token.equalsIgnoreCase(operator)) return true;
		return false;
	}
	
	private void parseToken (Queue<String> tokens){
		String token = tokens.poll();
		if (token.equalsIgnoreCase(OB)) operators.push(token);
		else if (token.equalsIgnoreCase(CB))
			while(!operators.peek().equalsIgnoreCase(OB)) doOperationFor(operators.pop());
		else if (isOperator(token)){
			while(!operators.isEmpty() && isHigherPrecedence(operators.peek(),token))
				doOperationFor(operators.pop());
			operators.push(token);
		} else {
			String field = token;
			tokens.poll(); //discard the equals.
			String value = tokens.poll();
			values.push(buildBeanFor(field,value));
		}
	}

	public BeanCondition<T> resolveQuery(String query){
		logger.info("Resolving query: ["+query+"].");

		Queue<String> list = QueryTokenizer.makeTokenStream(query);
		logger.debug("Made token stream ["+list+"].");
		
		try {
			while (!list.isEmpty())	parseToken(list);					
			while (!operators.isEmpty()) doOperationFor(operators.pop());
		} catch(Exception e){
			logger.error("An exception occured parsing the query: "+query,e);
			return null;
		}
		BeanCondition<T> condition = null;
		
		if (values.isEmpty() || values.peek()==null){
			logger.debug("Bean condition could not be generated from query.["+query+"].");
			condition = new FalseBeanConditionImpl<T>();
		}
		else condition = values.pop();
		logger.debug("Constructed bean condition (in SQL format) ["+condition.toSQLFormat()+"].");
		return condition;
	}
}
