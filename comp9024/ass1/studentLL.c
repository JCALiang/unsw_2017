#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "studentLL.h"
#include "studentRecord.h"

// linked list node type
// DO NOT CHANGE
typedef struct node {
    studentRecordT data;
    struct node    *next;
} NodeT;

// linked list type
typedef struct ListRep {
   NodeT *head;
} ListRep;

/*** Your code for stages 2 & 3 starts here ***/

// Time complexity: O(1)
// Explanation: the algorithm time is constant on creating a new dynamic memory allocated list
List newLL() {
	ListRep *L= malloc(sizeof(ListRep));
	assert(L!=NULL);
	L-> head=NULL;
	return L;
	
}

// Time complexity: O(n)
// Explanation: a while loop that examine each node (n) in the list
void dropLL(List listp) {
	NodeT *current = listp-> head;
	while (current!= NULL){
		NodeT *temp = current->next;
		free(current);
		current=temp;}
	free(listp);
	return;
}

// Time complexity: O(n)
// Explanation: a while loop that examines each node (N) in the list
void inLL(List listp, int zid) {
	NodeT *current = listp->head;
	while (current!=NULL){
		if (current-> data.zID == zid){
			printStudentData(zid, current->data.credits,current->data.WAM);
				return;
		}
		current=current->next;
	}
	
	printf("No record found.\n");
	return;
}

// Time complexity: O(n)
// Explanation: 2 independent while loops, O(2n) simplifies to O(n)
void insertLL(List listp, int zid, int cr, float wam) {
	
	/* set up new node */
	NodeT *new= malloc(sizeof(NodeT));	
	assert(new!=NULL);
	new->data.zID= zid;
	new->data.credits=cr;
	new->data.WAM=wam;
	NodeT *current=listp->head;
	
	/* check if head is empty */
	
	if (listp->head ==NULL){
		new->next= listp->head;
		listp->head=new;
		printf("Student record added.\n");
		return;}
	
	/* check if new value is smaller than listp head */
	
	if (new->data.zID < listp->head->data.zID){
		new->next=listp->head;
		listp->head=new;
		printf("Student record added.\n");
		return;}
	
	/* check if its equal */
	while (current!=NULL){
		if (current->data.zID== new->data.zID){
			current->data=new->data;
			printf("Student record updated.\n");
			return;
		}
		current=current->next;
	}
	
	current=listp->head;
	/* check the position, if current value is smaller, keep looping */
	while (current->next!=NULL){
		if (current->next->data.zID > new->data.zID){
			break;}
		current=current->next;}
	
	new->next=current->next;
	current->next=new;
	printf("Student record added.\n");
	return;
	
}


// Time complexity: O(n)
// Explanation: one while loop that examines each node in the list
void getStatLL(List listp, int *n, float *wam, float *w_wam) {
	 int sumcredit=0;

	 NodeT *current= listp->head;
	while(current!=NULL){
		*n+=1;
		*wam+= current->data.WAM;
		 *w_wam+= current->data.WAM * current->data.credits;
		 sumcredit+= current->data.credits;
		current=current->next;
		};
	   *wam=*wam/ *n;
	   *w_wam= *w_wam/sumcredit;
		return;
}

// Time complexity:  O(n)
// Explanation: one while loop examines each node in the list
void showLL(List listp) {
	int zID, cr;
	float wam;
	NodeT *current= listp->head;
	while (current!=NULL){
		zID= current-> data.zID;
		cr= current->data.credits;
		wam=current->data.WAM;
		printStudentData(zID, cr, wam);
		current=current->next;}
	return;
}
