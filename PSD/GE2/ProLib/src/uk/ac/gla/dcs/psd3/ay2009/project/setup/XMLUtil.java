package uk.ac.gla.dcs.psd3.ay2009.project.setup;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import org.apache.log4j.Logger;
import org.marc4j.MarcReader;
import org.marc4j.MarcXmlReader;
import org.marc4j.marc.Record;

import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

/**
 * Utility methods for extracting a list of MARC book records from an input source.
 * @author tws
 *
 */
public class XMLUtil {
	
	public static final Logger logger =  L4JConfiguredLoggerFactory.getConfiguredL4JLogger(XMLUtil.class);

	/**
	 * @param file a compressed (zip format) file. The first entry of the 
	 * zip file must be an XML file representation of a list of MARC records.
	 * @return a list of MARC record objects, or null if the zip file is 
	 * corrupt.
	 */
	public static List<Record> getMARCRecordsFromCompressedXMLFile (ZipFile file){
		List<Record> records = null;
		try {
			//Assume zip archive contains a single entry.
			ZipEntry ze = file.entries().nextElement();
			InputStream is = file.getInputStream(ze);
			records = getMARCRecordsFromInputStream(is);
		} catch (IOException e) {
			logger.error("While attempting to construct an input stream from archive ["+file.getName()+"].",e);
		} 
		return records;
	}	
	
	/**
	 * @param file an XML file representation of a list of MARC records.
	 * @return a list of MARC record objects, or null if the file is 
	 * corrupt.
	 */
	public static List<Record> getMARCRecordsFromXMLFile (File file){
		 InputStream is = null;
			try {
				is = new FileInputStream(file);
			} catch (FileNotFoundException e) {				
				logger.error("Couldn't find XML file ["+file.getAbsolutePath()+"].",e);
			}
			return getMARCRecordsFromInputStream(is);
	}
	
	/**
	 * @param is the source for a list of XML formatted MARC records.
	 * @return a list of MARC record objects.  The list may be empty if the 
	 * input stream is corrupt.
	 */
	public static List<Record> getMARCRecordsFromInputStream (InputStream is){
		 List<Record> records = new ArrayList<Record>();
		 MarcReader reader = new MarcXmlReader(is);
		 
		 while (reader.hasNext()) {
			 Record record = reader.next();
			 records.add(record);
		 }		 
		return records;
	}
}
