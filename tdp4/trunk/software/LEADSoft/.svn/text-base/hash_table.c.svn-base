#include "hash_table.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#ifdef HASH_DEBUG
	#include <stdarg.h>
#endif

/* ========================================================================
 * Table of CRC-32's of all single-byte values (made by make_crc_table)
 */
static const unsigned long crc_table[256] = {
  0x00000000L, 0x77073096L, 0xee0e612cL, 0x990951baL, 0x076dc419L,
  0x706af48fL, 0xe963a535L, 0x9e6495a3L, 0x0edb8832L, 0x79dcb8a4L,
  0xe0d5e91eL, 0x97d2d988L, 0x09b64c2bL, 0x7eb17cbdL, 0xe7b82d07L,
  0x90bf1d91L, 0x1db71064L, 0x6ab020f2L, 0xf3b97148L, 0x84be41deL,
  0x1adad47dL, 0x6ddde4ebL, 0xf4d4b551L, 0x83d385c7L, 0x136c9856L,
  0x646ba8c0L, 0xfd62f97aL, 0x8a65c9ecL, 0x14015c4fL, 0x63066cd9L,
  0xfa0f3d63L, 0x8d080df5L, 0x3b6e20c8L, 0x4c69105eL, 0xd56041e4L,
  0xa2677172L, 0x3c03e4d1L, 0x4b04d447L, 0xd20d85fdL, 0xa50ab56bL,
  0x35b5a8faL, 0x42b2986cL, 0xdbbbc9d6L, 0xacbcf940L, 0x32d86ce3L,
  0x45df5c75L, 0xdcd60dcfL, 0xabd13d59L, 0x26d930acL, 0x51de003aL,
  0xc8d75180L, 0xbfd06116L, 0x21b4f4b5L, 0x56b3c423L, 0xcfba9599L,
  0xb8bda50fL, 0x2802b89eL, 0x5f058808L, 0xc60cd9b2L, 0xb10be924L,
  0x2f6f7c87L, 0x58684c11L, 0xc1611dabL, 0xb6662d3dL, 0x76dc4190L,
  0x01db7106L, 0x98d220bcL, 0xefd5102aL, 0x71b18589L, 0x06b6b51fL,
  0x9fbfe4a5L, 0xe8b8d433L, 0x7807c9a2L, 0x0f00f934L, 0x9609a88eL,
  0xe10e9818L, 0x7f6a0dbbL, 0x086d3d2dL, 0x91646c97L, 0xe6635c01L,
  0x6b6b51f4L, 0x1c6c6162L, 0x856530d8L, 0xf262004eL, 0x6c0695edL,
  0x1b01a57bL, 0x8208f4c1L, 0xf50fc457L, 0x65b0d9c6L, 0x12b7e950L,
  0x8bbeb8eaL, 0xfcb9887cL, 0x62dd1ddfL, 0x15da2d49L, 0x8cd37cf3L,
  0xfbd44c65L, 0x4db26158L, 0x3ab551ceL, 0xa3bc0074L, 0xd4bb30e2L,
  0x4adfa541L, 0x3dd895d7L, 0xa4d1c46dL, 0xd3d6f4fbL, 0x4369e96aL,
  0x346ed9fcL, 0xad678846L, 0xda60b8d0L, 0x44042d73L, 0x33031de5L,
  0xaa0a4c5fL, 0xdd0d7cc9L, 0x5005713cL, 0x270241aaL, 0xbe0b1010L,
  0xc90c2086L, 0x5768b525L, 0x206f85b3L, 0xb966d409L, 0xce61e49fL,
  0x5edef90eL, 0x29d9c998L, 0xb0d09822L, 0xc7d7a8b4L, 0x59b33d17L,
  0x2eb40d81L, 0xb7bd5c3bL, 0xc0ba6cadL, 0xedb88320L, 0x9abfb3b6L,
  0x03b6e20cL, 0x74b1d29aL, 0xead54739L, 0x9dd277afL, 0x04db2615L,
  0x73dc1683L, 0xe3630b12L, 0x94643b84L, 0x0d6d6a3eL, 0x7a6a5aa8L,
  0xe40ecf0bL, 0x9309ff9dL, 0x0a00ae27L, 0x7d079eb1L, 0xf00f9344L,
  0x8708a3d2L, 0x1e01f268L, 0x6906c2feL, 0xf762575dL, 0x806567cbL,
  0x196c3671L, 0x6e6b06e7L, 0xfed41b76L, 0x89d32be0L, 0x10da7a5aL,
  0x67dd4accL, 0xf9b9df6fL, 0x8ebeeff9L, 0x17b7be43L, 0x60b08ed5L,
  0xd6d6a3e8L, 0xa1d1937eL, 0x38d8c2c4L, 0x4fdff252L, 0xd1bb67f1L,
  0xa6bc5767L, 0x3fb506ddL, 0x48b2364bL, 0xd80d2bdaL, 0xaf0a1b4cL,
  0x36034af6L, 0x41047a60L, 0xdf60efc3L, 0xa867df55L, 0x316e8eefL,
  0x4669be79L, 0xcb61b38cL, 0xbc66831aL, 0x256fd2a0L, 0x5268e236L,
  0xcc0c7795L, 0xbb0b4703L, 0x220216b9L, 0x5505262fL, 0xc5ba3bbeL,
  0xb2bd0b28L, 0x2bb45a92L, 0x5cb36a04L, 0xc2d7ffa7L, 0xb5d0cf31L,
  0x2cd99e8bL, 0x5bdeae1dL, 0x9b64c2b0L, 0xec63f226L, 0x756aa39cL,
  0x026d930aL, 0x9c0906a9L, 0xeb0e363fL, 0x72076785L, 0x05005713L,
  0x95bf4a82L, 0xe2b87a14L, 0x7bb12baeL, 0x0cb61b38L, 0x92d28e9bL,
  0xe5d5be0dL, 0x7cdcefb7L, 0x0bdbdf21L, 0x86d3d2d4L, 0xf1d4e242L,
  0x68ddb3f8L, 0x1fda836eL, 0x81be16cdL, 0xf6b9265bL, 0x6fb077e1L,
  0x18b74777L, 0x88085ae6L, 0xff0f6a70L, 0x66063bcaL, 0x11010b5cL,
  0x8f659effL, 0xf862ae69L, 0x616bffd3L, 0x166ccf45L, 0xa00ae278L,
  0xd70dd2eeL, 0x4e048354L, 0x3903b3c2L, 0xa7672661L, 0xd06016f7L,
  0x4969474dL, 0x3e6e77dbL, 0xaed16a4aL, 0xd9d65adcL, 0x40df0b66L,
  0x37d83bf0L, 0xa9bcae53L, 0xdebb9ec5L, 0x47b2cf7fL, 0x30b5ffe9L,
  0xbdbdf21cL, 0xcabac28aL, 0x53b39330L, 0x24b4a3a6L, 0xbad03605L,
  0xcdd70693L, 0x54de5729L, 0x23d967bfL, 0xb3667a2eL, 0xc4614ab8L,
  0x5d681b02L, 0x2a6f2b94L, 0xb40bbe37L, 0xc30c8ea1L, 0x5a05df1bL,
  0x2d02ef8dL
};


/* ========================================================================= */
#define DO1(buf) crc = crc_table[((int)crc ^ (*buf++)) & 0xff] ^ (crc >> 8);
#define DO2(buf)  DO1(buf); DO1(buf);
#define DO4(buf)  DO2(buf); DO2(buf);
#define DO8(buf)  DO4(buf); DO4(buf);

/* ========================================================================= */
unsigned long crc32(unsigned long crc, const unsigned char *buf, unsigned int len)
{
	if (buf == NULL)
		return 0L;

	crc = crc ^ 0xffffffffL;
	while (len >= 8)
	{
		DO8(buf);
		len -= 8;
	}

	if (len)
		do
		{
			DO1(buf);
		}
		while (--len);

	return crc ^ 0xffffffffL;
}

struct hashitem_t
{
	char* name;
	void* data;
	/*
	 * In case there is a hash collision, then items at that location will act
	 * as a linked list.
	 */
	struct hashitem_t* next;
};

typedef struct hashitem_t hashitem;

struct hashtable_t
{
	hashitem* start;
	unsigned int size;
	hash_fn hash;
};

int debug(const char *fmt, ...)
{
	#ifdef HASH_DEBUG
	va_list ap;
	int r = 0;

	va_start(ap, fmt);
	r = vfprintf(stderr, fmt, ap);
	va_end(ap);

	return r;
	#else
	return 0;
	#endif
}

unsigned int default_hash_function(const char* name)
{
	return crc32(0, (unsigned char*)name, strlen(name));
}

hashtable* ht_init(unsigned int table_size, hash_fn fn)
{
	hashtable* ht = (hashtable*)malloc(sizeof(hashtable));

	if (!ht)
		return NULL;

	debug("Initialization of table [%p] with size %u\n", ht, table_size);

	ht->size = table_size;

	/* Allocate and zero the hash table. */
	ht->start = (hashitem*)calloc(table_size, sizeof(hashitem));

	if (!ht->start)
	{
		free(ht);
		return NULL;
	}

	if (!fn)
	{
		/* Use internal hash function. */
		ht->hash = default_hash_function;
		debug ("Using internal (CRC32) hash\n");
	}
	else
	{
		/* Use the supplied hash function. */
		ht->hash = fn;
		debug("Using user-supplied hash\n");
	}

	debug("Initialization successful\n\n");

	return ht;
}

int ht_add(hashtable* ht, const char* name, void* data)
{
	hashitem *dest, *test;

	/* Do some basic sanity-checking. */
	if (!ht || !name)
		return 1;

	debug("Adding %s [%p]\n", name, data);

	/* Calculate where in the table this entry should live. */
	dest = &ht->start[ht->hash(name) % ht->size];
	debug("dest: [%p]\n", dest);

	/* Use another point to recursively check all entries at the location. */
	test = dest;

	while (test && test->name)
	{
		/* An entry exists at this location, check it. */
		if (!strcmp(test->name, name))
		{
			/* The names match, so return 0 to signify success. */
			debug("Already got it\n");
			return 0;
		} 
		else
		{
			/* The names dont match, so check the next entry. */
			debug("HASH COLLISION!!\n");
			test = test->next;
		}
	}

	/* If we reach here, then we must add the item to the hashtable. */
	if (dest->name)
	{
		/*
		 * There is already an item at this location, we'll have to
		 * allocate a new item and append to this location.
		 */
		while (dest->next)
		{
			dest = dest->next;
		}
		/* We are now on the last item of the linked list at the location. */
		dest->next = (hashitem*)calloc(1, sizeof(hashitem));

		dest = dest->next;
		/* Check that the allocation didnt fail. */
		if (!dest) return 1;

	}

	dest->name = strdup(name);
	dest->data = data;
	/* dest->next is already 0 thanks to calloc */
	debug("Adding done\n\n");

	return 0;
}

int ht_add_ncase(hashtable* ht, const char* name, void* data)
{
	unsigned int x;
	char* name2;
	int rc = 0;

	name2 = strdup(name);

	if (!name2) return 1;

	/* TODO: Could use some optimization */
	for (x=0; x<strlen(name2); x++)
	{
		name2[x] = tolower(name2[x]);
	}

	rc = ht_add(ht, name2, data);

	free(name2);

	return rc;
}

int ht_remove(hashtable* ht, const char* name, int clean)
{
	hashitem *src;
	hashitem *prev;
	unsigned int pos;

	/* Do some basic sanity-checking. */
	if (!ht || !name)
		return 1;

	debug("Looking for %s\n", name);

	/* Calculate where in the table this entry should be. */
	pos = ht->hash(name) % ht->size;

	prev = NULL;
	for (src = &ht->start[pos]; src != NULL; src = src->next)
	{
		if (src->name != NULL && strcmp(src->name, name) == 0)
		{
			/* We found the key */
			hashitem *next = src->next;

			/* free what need to be freed */
			free(src->name);
			if (clean != 0)
				free(src->data);

			if (prev == NULL)
			{
				/* dealing with the main entry */
				memset(src, 0, sizeof(hashitem));

				if (next != NULL)
				{
					src->name = next->name;
					src->data = next->data;
					src->next = next->next;

					free(next);
				}
			}
			else
			{
				/* dealing with one of the link list item */
				prev->next = next;
				free(src);
			}

			return 0;
		}
		prev = src;
	}

	return 1;
}

int ht_lookup(hashtable* ht, const char* name, void** data)
{
	hashitem *src;

	/* Do some basic sanity-checking. */
	if (!ht || !name)
		return 1;

	debug("Looking for %s\n", name);

	/* Calculate where in the table this entry should be. */
	src = &ht->start[ht->hash(name) % ht->size];

	debug("src: [%p]\n", src);

	while (src && src->name)
	{
		if (!strcmp(src->name, name))
		{
			/* Found the item, return it if they supplied storage. */
			debug("Found the item at [%p]\n", src);

			if (data)
				*data = src->data;
			
			/* Return success. */
			return 0;
		} 
		else
		{
			/* Names dont match, check any other entries at this location. */
			src = src->next;
		}
	}

		debug("Item not found\n\n");

	/* If we reached here, the entry was not found, so return failure. */
	return 1;
}

int ht_lookup_ncase(hashtable* ht, const char* name, void** data)
{
	unsigned int x;
	char* name2;
	int rc = 0;

	name2 = strdup(name);

	if (!name2)
		return 1;

	/* TODO: Could use some optimization */
	for (x=0; x<strlen(name2); x++)
	{
		name2[x] = tolower(name2[x]);
	}

	rc = ht_lookup(ht, name2, data);

	free(name2);

	return rc;
}

void ht_destroy(hashtable* ht)
{
	unsigned int x;
	hashitem *item, *prev, *next;

	/* Do some basic sanity-checking. */
	if (!ht)
		return;

	debug("Destroy called on [%p]\n", ht);

	/*
	 * TODO: This could probably use some optimization, even just having a
	 *	   doubly-linked list would help, at the cost of memory.
	 */
	for (x = 0; x < ht->size; x++)
	{
		item = &ht->start[x];

		if (item->name)
			free(item->name);

		while(1)
		{
			prev = item;
			next = item->next;

			if (!next)
				break;

			while (next->next)
			{
				next = next->next;
			}

			free(next->name);
			free(prev->next);
			prev->next = NULL;
		}
	}

	debug("Destroy complete\n\n");
}

int ht_serialize(hashtable* ht, const char *filepath, serialize_fn fn)
{
	unsigned int i;
	hashitem *item;

	if (filepath == NULL)
	{
		debug("filepath is null\n");
		return 1;
	}

	FILE *fp = fopen(filepath, "w+");
	if (fp == NULL)
	{
		debug("Unable to open %s\n", filepath);
		return 1;
	}

	/* Iterate through the hashtable items */
	for (i = 0; i < ht->size; i++)
	{
		/* Iterate through the hashtable element linked list */
		for (item = &ht->start[i]; item != NULL; item = item->next)
		{
			if (item->name != NULL)
			{
				if (fn == NULL)
				{
					debug("adding element without serialization function\n");
					fprintf(fp, "%s=%s\n", item->name, (char *)(item->data));
				}
				else
				{
					debug("adding element using serialization function\n");
					char *ser_value = fn(item->data);
					fprintf(fp, "%s=%s\n", item->name, ser_value);
					free(ser_value);
				}
			}
		}
	}
	
	fclose(fp);
	return 0;
}

int ht_deserialize(hashtable* ht, char *filepath, deserialize_fn fn)
{
	char *buffer;
	char *ret;

	if (filepath == NULL)
	{
		debug("filepath is null\n");
		return 1;
	}

	FILE *fp = fopen(filepath, "r");
	if (fp == NULL)
	{
		debug("Unable to open %s\n", filepath);
		return 1;
	}

	/* allocate plenty of space to store one line */
	buffer = malloc(1024);

	/* read line by line */
	while ((ret = fgets(buffer, 1024, fp)) != NULL)
	{
		int len = strlen(ret);
		debug(ret);

		if (len == 1 || ret[0] == '#')
			continue;

		/* remove the trailing newline */
		ret[len - 1] = 0;

		/* parse the key=value pair */
		char *delim = strchr(ret, '=');
		if (delim == NULL)
		{
			debug("Unable to find the delimiter\n");
			continue;
		}

		char *key = strndup(ret, delim - ret);
		char *value = strdup(delim + 1);

		debug("key : %s  value : %s\n", key, value);

		/* add the entry to the hashtable */
		if (fn == NULL)
		{
			debug("adding element without deserialization function\n");
			ht_add(ht, key, value);
		}
		else
		{
			debug("adding element with deserialization function\n");
			ht_add(ht, key, fn(value));
		}

		/* a copy of the key is also made in ht_add() */
		free(key);
	}

	/* house keeping */
	fclose(fp);
	free(buffer);
	return 0;
}
