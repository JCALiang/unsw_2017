#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "Graph.h"
#include "queue.h" 
#define MAX_WORD_LENGTH 19
#define MAX_WORDS 1000
#define minimum(i,j,k) ((i)<(j)? ((i) < (k) ? (i) : (k)) : ((j) < (k) ? (j) : (k))) //refer from wikipedia

typedef char a[Max_Word][Max_Word_Length];

int compare(char *s1, char *s2, int len1, int len2){
	if (len1 ==0){
		return len2;}
	if (len2 ==0) {
		return len1;}
	
	int dist=0;
	if (s1[len1-1] != s2[len2-1]){
		dist=1;}
	
	return minimum(compare(s1, s2, len1-1, len2)   +1,
				   compare(s1, s2, len1,   len2-1)   +1,
				   compare(s1, s2, len1-1, len2-1) + dist);
}

int *intdup(int const *original, int len){
		int *copy= malloc(len*sizeof(int));
		memcpy(copy, original, len*sizeof(int));
		return copy;
}

void print_stack(int* path, int index, a array){
	for (int i=0; i < index ; i++){
		if (i==index-1){
			printf("%s", array[path[i]]);}
		else{
			printf("%s -> ", array[path[i]]);}
	}
}

int longest;
int* chain_array[MAX_WORDS];

void findPath(int src, int dest, int indx, int n, int dup, int* path, int* visited, Graph g){
	visited[src]= true;
	path[indx]=src;
	indx++;

	if (src==dest){
		if (indx>longest){
			memset (chain_array, 0, sizeof(chain_array));
			longest=indx;
			int* longest_chain = intdup(path, indx);
			dup=0;
			chain_array[dup] = longest_chain;}
		 else if (indx == longest){
			dup++;
			 printf("equal\n");
			int* longest_chain = intdup(path, indx);
			chain_array[dup]= longest_chain;
		} else {
			int k;
		}
	}else{
		for (int i=src; i<n; i++){
			if (visited[i]==false &&  adjacent(g,src,i)){
				findPath(i, dest, indx, n, dup, path, visited, g);
			}
		}
	}
	visited[src]=false;
	indx--;
}

int main (void){
	int n;
	char array[MAX_WORDS][MAX_WORD_LENGTH];
	
	//initialize new graph
	printf("Enter a number: ");
	scanf("%d", &n);
	Graph g = newGraph(n);
	
	//create array of words list
	for (int i=0; i<n; i++){
		printf("Enter word: ");
		scanf("%s", array[i]);
	}
	printf("\n");
	Edge e;
	
	//task 1 implementation : insert edge
	//time complexity: horrible
	//				Levenshtein distance under recursion is 2^n
	//              a double for loop to iterate wordlist twice: n^2
	//             overall complexity: n^2 * 2^n= O(2^n) which is polynomial
	for (int j=0; j<n; j++){
		for (int k= j+1; k<n; k++){
			int len1 = strlen(array[j]);
			int len2 = strlen(array[k]);
			if (compare(array[j], array[k], len1, len2)==1){
				e.v=j;
				e.w=k;
				insertEdge(g, e);
			}
		}
	}

	
	//task 2: find the maximum length of the word chain
	// time complexity: O(n*n!)
	
	if (n==1){
		int longest=1;
		int* longest_chain= 0 ;
		
	} else {
		
	for (int jj=1; jj<n; jj++){
		int path[n];
		int visited[n];
		int indx=0;
		int dup=0;
		memset (visited, 0, sizeof(visited));

		findPath(0, jj, indx, n, dup, path, visited, g);
		}
	}
	showGraph(g, array);
	printf("\n");
	printf("Maximum chain length: %d\n", longest);
	printf("Maximal chains:\n");
	for (int i=0; i<n; i++){
		if (chain_array[i]!=0){
			int* longest_chain = chain_array[i];
			print_stack(longest_chain, longest, array);
			printf("\n");}
	}

	freeGraph(g);
	return 0;
}
		