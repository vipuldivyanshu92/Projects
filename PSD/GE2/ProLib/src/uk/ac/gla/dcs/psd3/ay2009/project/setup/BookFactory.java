package uk.ac.gla.dcs.psd3.ay2009.project.setup;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.zip.ZipFile;

import org.apache.log4j.Logger;
import org.marc4j.marc.DataField;
import org.marc4j.marc.Record;
import org.marc4j.marc.Subfield;

import uk.ac.gla.dcs.psd3.ay2009.project.model.Book;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookDescription;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookDescriptionImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.BookImpl;
import uk.ac.gla.dcs.psd3.ay2009.project.model.Book.Status;
import uk.ac.standrews.cs.l4jconfig.L4JConfiguredLoggerFactory;

/**
 * Provides intermediate bean representations of MARC book records. 
 * @author tws
 */
public class BookFactory {

	private static final Logger logger =  L4JConfiguredLoggerFactory.getConfiguredL4JLogger(BookFactory.class);

	private static final String zipFileName = "config/descriptions.zip";
	private static final String cacheFileName = "config/descriptions.obj";
	
	/**
	 * Creates a list of book instances from a standard set of book descriptions. 
	 * @return a list of book instances.
	 */
	public static List<Book> createBooks(Integer numBooks){
		List<Book> books = new ArrayList<Book>();

		List<BookDescription> bookDescriptions = loadBookDescriptions();
		if (bookDescriptions == null || bookDescriptions.size() == 0){
			
			bookDescriptions = getBookDescriptionsFromZipFile();
			saveBookDescriptions(bookDescriptions);
			
			if (bookDescriptions == null){
				logger.warn("Couldn't obtain any information on books.");
				return books;
			}
		}
		logger.debug("Found ["+bookDescriptions.size()+"] book descriptions.");
				
		Random r = new Random();
		
		for (int i = 0; i < numBooks; i++){
			
			BookDescription description = bookDescriptions.get(r.nextInt(bookDescriptions.size()));	
			Book book = new BookImpl(i,Status.IN_LIBRARY,description);
			books.add(book);	
		}
			
		logger.debug("Created ["+books.size()+"] books.");
		return books;
	}
	
	@SuppressWarnings("unchecked")
	private static List<BookDescription> loadBookDescriptions(){
		File file = new File(cacheFileName);
		ObjectFileStore<List> ofs = new ObjectFileStore<List>(file,ArrayList.class);
		return ofs.loadObject();		
	}
	
	@SuppressWarnings("unchecked")
	private static void saveBookDescriptions(List<BookDescription> descriptions) {
		File file = new File(cacheFileName);
		ObjectFileStore<List> ofs = new ObjectFileStore<List>(file,ArrayList.class);
		ofs.saveObject(descriptions);		
	}
	
	private static List<BookDescription> getBookDescriptionsFromZipFile(){
		ZipFile zf = getRecordsFile(zipFileName);
		if (zf == null){
			logger.warn("Couldn't open archive ["+zipFileName+"] to initialise database.\n");
			return null;
		}
		
		List<Record> records = XMLUtil.getMARCRecordsFromCompressedXMLFile(zf);
		
		List<BookDescription> descriptions = new ArrayList<BookDescription>();

		int count = 0;
		for (Record record: records){
			BookDescription description = getBookDescription(record);
			description.setID(count++);
			descriptions.add(description);
		}
		return descriptions;
	}	
	
	private static ZipFile getRecordsFile(String zipFileName){
		ZipFile zf = null;
		try {
			zf = new ZipFile(zipFileName);
		} catch (IOException e) {
			logger.error("While accessing archive ["+zipFileName+"].",e);
		}		
		return zf;
	}
	
	private static BookDescription getBookDescription(Record record){
		BookDescription bookDescription = new BookDescriptionImpl(
				getPrettyTitle(record), 
				getPrettyAuthors(record),
				getPrettyPublicationDate(record),
				getPrettyPublisher(record),
				getPrettyISBN(record),
				0
				);
		
		return bookDescription;
	}

	private static String getPrettyTitle (Record record){
		String pretty_title = getFieldData(record,"245",'a');
		pretty_title += getFieldData(record,"245",'b');
		pretty_title += getFieldData(record,"245",'p');

		return pretty_title.replace('\'', ' ');
	}
	
	private static String getPrettyPublicationDate(Record record){
		return getFieldData(record,"260",'c').replace('\'', ' ');
	}
	
	private static String getPrettyPublisher(Record record) {
		return getFieldData(record,"260",'b').replace('\'', ' ');
	}

	private static String getPrettyAuthors(Record record) {
		String pretty_authors  = getFieldData(record,"100",'a');
		
		if (pretty_authors == "") pretty_authors = getFieldData(record,"110",'a');
		if (pretty_authors == "") pretty_authors = getFieldData(record,"111",'a');
		if (pretty_authors == "") return null;
		
		String pretty_authors_p = getFieldData(record,"700",'a');
		if (pretty_authors_p != "") pretty_authors += ", "+pretty_authors_p; 
		String pretty_authors_c = getFieldData(record,"710",'a');
		if (pretty_authors_c != "") pretty_authors += ", "+pretty_authors_c; 
		String pretty_authors_m = getFieldData(record,"711",'a');
		if (pretty_authors_m != "") pretty_authors += ", "+pretty_authors_m; 
		
		return pretty_authors.replace('\'', ' ');
	}
		
	private static String getPrettyISBN(Record record) {
		String ISBN = getFieldData(record,"020",'a');
		return ISBN.replace('\'', ' ');
	}
		
	private static String getFieldData(Record record, String tag, char sf_code){
		DataField df = (DataField)record.getVariableField(tag);
		if (df != null){
			Subfield sf = df.getSubfield(sf_code); 
			if (sf !=null)
				return sf.getData().replace('\'', ' ');
			else return "";
		}
		else return "";
	}
}
