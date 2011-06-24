#include <stdio.h>
#include <stdlib.h>
#include "LinkedList.h"



LinkedList * ll_create(){
	LinkedList * list = (LinkedList*)malloc(sizeof(LinkedList));
	list->size = 0;
	list->head = NULL;
	list->tail = NULL;
	return list;
}

void ll_destroy(LinkedList * list){
	if(list->size == 0){
		free(list);
	}
}
	
void ll_add(LinkedList * l, void* value){
	LNode * n = (LNode*) malloc(sizeof(LNode));
	
	if (l->head == NULL){
		l->head = n;
	}
	else{
		l->tail->next = n;
	}	
	n->data = value;
	n->next = NULL;
	l->tail = n;
	l->size++;
		
}

void* ll_get(LinkedList * l){
	if (l->size > 0){
		LNode* t = l->head;
		void* tmp = t->data;
		l->head = t->next;
		free(t);
		l->size--;
		return tmp;
	}
	else
		return NULL;

}
/*
int main (int argc, char const *argv[])
{
	LinkedList* list = ll_create();
	int x = 0;
	int i = 1;
	int j = 2;
	int k = 3;
	int l = 4;
	ll_add(list, &i);
	ll_add(list, &j);
	ll_add(list, &k);
	ll_add(list, &l);
	
	x = *((int*)ll_get(list));
	if (x != 0)
		printf("Value: %d\n", x);
	else
		printf("Value was NULL!!");
	
	x = *((int*)ll_get(list));
	if (x != 0)
		printf("Value: %d\n", x);
	else
		printf("Value was NULL!!");
	
	x = *((int*)ll_get(list));
	if (x != 0)
		printf("Value: %d\n", x);
	else
		printf("Value was NULL!!");
	
	x = *((int*)ll_get(list));
	if (x != 0)
		printf("Value: %d\n", x);
	else
		printf("Value was NULL!!");
	
	ll_destroy(list);
	
	return 0;
}*/
