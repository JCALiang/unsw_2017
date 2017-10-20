// Graph ADT interface ... COMP9024 17s2
#include <stdbool.h>
#define Max_Word 1000
#define Max_Word_Length 19

typedef struct GraphRep *Graph;

// vertices are ints
typedef int Vertex;

//array size are tailor to the specs
typedef char array[Max_Word][Max_Word_Length];


// edges are pairs of vertices (end-points)
typedef struct Edge {
   Vertex v;
   Vertex w;
} Edge;

Graph newGraph(int);
void  insertEdge(Graph, Edge);
void  removeEdge(Graph, Edge);
bool  adjacent(Graph, Vertex, Vertex);
void  showGraph(Graph, array);
void  freeGraph(Graph);
