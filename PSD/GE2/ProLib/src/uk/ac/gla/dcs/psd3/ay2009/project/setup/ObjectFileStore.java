package uk.ac.gla.dcs.psd3.ay2009.project.setup;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;

import org.apache.log4j.Logger;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

public class ObjectFileStore<T> implements ObjectStore<T>{
	
	private static final Logger logger = L4JConfiguredLoggerFactory.getConfiguredL4JLogger(ObjectFileStore.class);
	
	private File f;
	private Class<? extends T> _impl;
	
	public ObjectFileStore(File f, Class<? extends T> _impl){
		this.f = f;
		this._impl = _impl;
	}
	
	@SuppressWarnings("unchecked")
	public T loadObject(){
		try {
			if (!f.exists()) {
				logger.debug("Couldn't find file ["+f.getName()+"], using new index.");
				return _impl.newInstance();
			} else {
				logger.debug("Found file ["+f.getName()+"], attempting to de-serialise");
				try{ 
					return (T)loadObject(new FileInputStream(f));
				}catch (ClassCastException cce){
					logger.error("Unexpected object type after de-serialisation.");
					return null;
				}
			}
		} catch (FileNotFoundException e) {
			logger.error("Couldn't find file ["+f+"]",e);
		} catch (InstantiationException e) {
			logger.error("Couldn't instantiate implementation class. ["+_impl+"].");
		} catch (IllegalAccessException e) {
			logger.error("Couldn't use default constructor in implementation class. ["+_impl+"].");
		} 
		return null;
	}

	public void saveObject(Object o) {
		try {
			logger.debug("Saving object to file ["+f+"].");
			if (!f.exists()) f.createNewFile();
			saveObject(o,new FileOutputStream(f));
		} catch (FileNotFoundException e) {
			logger.debug("Couldn't open file ["+f+"].",e);
		} catch (IOException e) {
			logger.debug("Couldn't write to file ["+f+"].",e);
		}
	}
		
	private static Object loadObject(InputStream is){
		try {
			ObjectInputStream ois = new ObjectInputStream(is);
			Object object = ois.readObject();
			ois.close();
			return object;
		} catch (IOException e) {
			logger.error("Couldn't open input Stream. ["+is+"]",e);
		} catch (ClassNotFoundException e) {
			logger.error("Couldn't de-serialise object from stream ["+is+"].",e);
		}
		return null;
	}
	
	private static void saveObject(Object o, OutputStream os) {
		try {
			ObjectOutputStream oos = new ObjectOutputStream(os);
			oos.writeObject(o);
			oos.close();
		} catch (IOException e) {
			logger.error("Couln't write object ["+o+"] to output stream ["+os+"]",e);
		}	
	}
}
