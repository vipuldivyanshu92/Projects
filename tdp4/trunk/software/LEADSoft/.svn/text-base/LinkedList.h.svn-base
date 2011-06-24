#include <stdio.h>
#include <stdlib.h>

typedef struct LNode{
	struct LNode* next;
	void* data;
	} LNode;

typedef struct LinkedList{
	LNode * head;
	LNode * tail;
	int size;
	} LinkedList;


LinkedList * ll_create();

void ll_destroy(LinkedList * list);

void ll_add(LinkedList * l, void* value);
	
void* ll_get(LinkedList * l);
	
