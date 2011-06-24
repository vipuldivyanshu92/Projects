#ifndef HASH_TABLE_H
#define HASH_TABLE_H

#ifdef __cplusplus
extern "C" {
#endif

/* The internal struct used for storing the hashtable. */
typedef struct hashtable_t hashtable;

/* The format of the hash function to be used by the hash table. */
typedef unsigned int (*hash_fn)(const char*);

/* Function used to serialize an element of the hashtable */
typedef char *(*serialize_fn)(void *);

/* Function used to deserialize an element to the hashtable */
typedef void *(*deserialize_fn)(const char *);

/* Initialize a hash table using the specified size.
   If fn is NULL, an internal hash function will be used.
   Returns a pointer to a hashtable object, used for identifying this table,
   or NULL if it fails to allocate enough memory. */
hashtable* ht_init(unsigned int table_size, hash_fn fn);

/* Add an item into the hash table.
   Returns 0 on success, anything else on failure. */
int ht_add(hashtable* ht, const char* name, void* data);

/* Same as above, but case-insensitive. */
int ht_add_ncase(hashtable* ht, const char* name, void* data);

/* Look up the given name and return its associated void* data if found.
   If the void** is NULL, the void* is not returned but the return value still
   indicates if the entry was found or not.
   Returns 0 on success, anything else on failure. */
int ht_lookup(hashtable* ht, const char* name, void** data);

/* Same as above, but case-insensitive. */
int ht_lookup_ncase(hashtable* ht, const char* name, void** data);

/* Serialize the hashtable in the file name specified, the serialize function
   takes a void* as parameter and should return a char* if NULL it is assumed
   that the data are a null terminated string. */
int ht_serialize(hashtable* ht, const char *filepath, serialize_fn fn);

/* Deserialize an hashtable from the file name specified, the deserialize
   function takes a char* as parameter and shoudl return a void* if NULL
   the data will be stored as a char*. */
int ht_deserialize(hashtable* ht, char *filepath, deserialize_fn fn);

/* Remove an item from the hashtable, if clean is non zero then the memory
   allocated for the data of this item will also be freed. */
int ht_remove(hashtable* ht, const char* name, int clean);

/* Free all the memory used by the hashtable. */
void ht_destroy(hashtable* ht);

#ifdef __cplusplus
}
#endif

#endif /* HASH_TABLE_H */
