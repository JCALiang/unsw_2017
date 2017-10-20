
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <ctype.h>

#include "studentRecord.h"
#include "studentLL.h"



void printHelp();
void StudentLinkedListProcessing();



int main(int argc, char *argv[]) {
   if (argc == 2) {
	int student_no;
	student_no= atoi(argv[1]);
	studentRecordT *students =malloc(student_no * sizeof(studentRecordT));
	assert(students != NULL);
									 
	int i;
	for (i=0; i<student_no; i++){
		students[i].zID= readValidID();
		students[i].credits= readValidCredits();
		students[i].WAM= readValidWAM();
		};
	   
	  
	 /*print out each student record store in the struct array*/
	 for (i=0; i<student_no; i++){
		printStudentData(students[i].zID, students[i].credits,students[i].WAM) ;
		};
	   
	   /* new variables to store avg_wam and w_wam*/
	 float avgwam=0;
	 float wavgwam=0;
	 int sumcredit=0;
	   
	 for (i=0; i<student_no; i++){
		avgwam+= students[i].WAM;
		 wavgwam+= (students[i].WAM * students[i].credits);
		 sumcredit+= students[i].credits;
		};
	 
	   avgwam=avgwam/student_no;
	   printf("Average WAM: %.3f\n", avgwam);
	   wavgwam= wavgwam/sumcredit;
	   printf("Weighted average WAM: %.3f\n", wavgwam);
	   
		free(students);
		
   } else {
      StudentLinkedListProcessing();
   }
   return 0;
}

/* Code for Stages 2 and 3 starts here */

void StudentLinkedListProcessing() {
   int op, ch;

   List list = newLL();   // create a new linked list
   
   while (1) {
      printf("Enter command (a,f,g,p,q, h for Help)> ");

      do {
	 ch = getchar();
      } while (!isalpha(ch) && ch != '\n');  // isalpha() defined in ctype.h
      op = ch;
      // skip the rest of the line until newline is encountered
      while (ch != '\n') {
	 ch = getchar();
      }
		int zID, cr, n=0;
		float rwam, wam=0, w_wam=0;
	
      switch (op) {

         case 'a':
         case 'A':
            		zID= readValidID();
					cr= readValidCredits();
					rwam= readValidWAM();
			  		insertLL(list,zID, cr, rwam);
	    break;

         case 'f':
         case 'F':
			zID= readValidID();
			  inLL(list, zID);
	    break;
	    
         case 'g':
         case 'G':
			  getStatLL(list, &n, &wam, &w_wam);
			  printf("Number of records: %d\n", n);
			  printf("Average WAM: %.3f\n", wam);
			   printf("Average weighted WAM: %.3f\n", w_wam);
	    break;
	    
         case 'h':
         case 'H':
            printHelp();
	    break;
	    
         case 'p':
         case 'P':
            showLL(list);
	    break;

	 case 'q':
         case 'Q':
            dropLL(list);       // destroy linked list before returning
	    printf("Bye.\n");
	    return;
      }
   }
}

void printHelp() {
   printf("\n");
   printf(" A - Add student record\n" );
   printf(" F - Find student record\n" );
   printf(" G - Get statistics\n" );
   printf(" H - Help\n");
   printf(" P - Print all records\n" );
   printf(" Q - Quit\n");
   printf("\n");
}
