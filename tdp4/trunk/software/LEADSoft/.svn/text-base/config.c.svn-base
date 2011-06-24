/*
 * File: config.cpp
 * Author: Simon Jouet
 * Style : Ansi-C
 *
 * Created on August 24, 2010, 15:14 PM
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "hash_table.h"

#define TABLE_SIZE  23    /* Better to use a prime number for hashtables size */
#define FILE_NAME   "configuration.conf"

typedef hashtable* config_t;

static int get_value(config_t config, char *name, void **data)
{
	hashtable *ht;
	int rc;

	ht = (hashtable *)config;
	rc = ht_lookup(ht, name, data);

	return rc;
}

config_t config_init()
{
    // Create the hashtable
    hashtable *ht = ht_init(TABLE_SIZE, NULL);

    // Load the file if it exists
    ht_deserialize(ht, FILE_NAME, NULL);

    return (config_t)ht;
}

int config_save(config_t config)
{
    hashtable *ht = (hashtable *)config;

    // Serialize the hashtable into a text file
    return ht_serialize(ht, FILE_NAME, NULL);
}

int config_release(config_t config)
{
	ht_destroy(config);
	return 0;
}

int config_get_dword(config_t config, char *name, int *value)
{
	void *data;

	if (get_value(config, name, &data) != 0)
		return 1;

	*value = atoi(data);
	return 0;
}

int config_get_string(config_t config, char *name, char **value)
{
	void *data;

	if (get_value(config, name, &data) != 0)
		return 1;

	*value = (char *)data;
	return 0;
}

int config_set_dword(config_t config, char *name, int value)
{
	hashtable *ht;
	char *key;
	int rc;

	ht = (hashtable *)config;
	key = name;

	char *s = malloc(10 + 1);	/* maximum length of 2^32 is 10 */
	sprintf(s, "%d", value);

	ht_remove(ht, key, 1);
	rc = ht_add(ht, key, s);

	return rc;
}

int config_set_string(config_t config, char *name, char *value)
{
	hashtable *ht;
	char *key;
	int rc;

	ht = (hashtable *)config;
	key = name;

	ht_remove(ht, key, 1);
	rc = ht_add(ht, key, strdup(value));

	return rc;
}
/*
int main()
{
	char *value;
	unsigned long dword;

	config_t config = config_init();

	config_set_dword(config, "HKLM", "test1", 123);
	config_set_string(config, "HKLM", "test2", "value");
	config_save(config);
	
	config_get_string(config, "HKLM", "test2", &value);
	printf("Value is : %s\n", value);

	config_get_dword(config, "HKLM", "test1", &dword);
	printf("Value is : %lu\n", dword);

	config_release(config);

	return EXIT_SUCCESS;
}
*/