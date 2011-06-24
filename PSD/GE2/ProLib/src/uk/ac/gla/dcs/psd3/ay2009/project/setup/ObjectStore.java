package uk.ac.gla.dcs.psd3.ay2009.project.setup;

public interface ObjectStore<T> {

	public abstract T loadObject();

	public abstract void saveObject(T o);

}