// Student record implementation ... Assignment 1 COMP9024 17s2
#include <stdio.h>

#define LINE_LENGTH 1024

// scan input for a positive floating point number, returns -1 if none
float readFloat(void) {
   char  line[LINE_LENGTH];
   float f;
   fgets(line, LINE_LENGTH, stdin);

   if ( (sscanf(line, "%f", &f) != 1) || f <= 0.0 )
      return -1;
   else
      return f;
}



// scan input for a positive integer, returns -1 if none
int readInt(void) {
   char line[LINE_LENGTH];
   int  n;

   fgets(line, LINE_LENGTH, stdin);
   if ( (sscanf(line, "%d", &n) != 1) || n <= 0 )
      return -1;
   else
      return n;
}


/*** Your code for stage 1 starts here ***/
int digit_number(int *temp){
	int count=0;
	int feed= *temp;
	while(feed!=0){
		count++;
		feed=feed/10;
		}
	if (count!=7) {
		return 1;}
	else {return 0;}
}


int readValidID(void) {
	
	printf("Enter student ID: ");

	int x= readInt();
	while(x<0 || digit_number(&x)){
		printf("Not valid. Enter a valid value: ");
		x=readInt();}
	
	return x;   
}



int readValidCredits(void) {
	printf("Enter credit points: ");
	int credit=readInt();
	
	while(credit<2 || credit>480){
		printf("Not valid. Enter a valid value: ");
		credit=readInt();}

	return credit;   
}

float readValidWAM(void) {
	printf("Enter WAM: ");
	float wam=readFloat();
	
	while(wam<50 || wam>100){
		printf("Not valid. Enter a valid value: ");
		wam=readFloat();}
	
	return wam;   	
}

void printStudentData(int zID, int credits, float WAM) {
	printf("------------------------\n" );
	printf("Student zID: z%d\n", zID);
	
	printf("Credits: %d\n", credits);
	char *level[]={"PS", "CR", "DN", "HD"};

	if (WAM>=85 && WAM<=100){
		printf("Level of performance: %s\n", level[3]);}
	else if (WAM>=75 && WAM<85){
		printf("Level of performance: %s\n", level[2]);}
	else if (WAM>=65 && WAM<75){
		printf("Level of performance: %s\n", level[1]);}
	else{
		printf("Level of performance: %s\n", level[0]);}
	

	printf("------------------------\n" );
}
