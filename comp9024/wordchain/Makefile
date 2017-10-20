wordchains: wordchains.c Graph.o queue.o
	gcc -o wordchains wordchains.c Graph.o queue.o
	
Graph.o: Graph.c Graph.h
	gcc -Wall -Werror -c Graph.c
	
queue.o: queue.c queue.h
	gcc -Wall -Werror -c queue.c