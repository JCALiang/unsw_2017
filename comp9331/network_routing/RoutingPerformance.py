#!/usr/bin/python

import sys
import random
import operator
import threading
import time

class Graph(object):
	def __init__(self, vertex, matrix=None, vlist=None):
		self.matrix=[[0]* vertex for _ in range(vertex)]
		self.nV=vertex;
		self.vlist=set();
		
	def insertEdge(self, v1, v2, weight):
		self.matrix[v1][v2]= weight
		self.matrix[v2][v1]= weight
		self.vlist.add(v1)
		self.vlist.add(v2)
		
	def add(self, v1, v2):
		self.matrix[v1][v2]+= 1
		self.matrix[v2][v1]+= 1
		
	def substract(self, v1, v2):
		self.matrix[v1][v2]-=1
		self.matrix[v2][v1]-=1
		
	def adjacent(self, v1, v2):
		return self.matrix[v1][v2]
		
	def Dijkstra(self, src, dest):
		distance={}
		predecessors={}
		confirmed=set()
		confirmed.add(src)
		q=self.vlist.copy()
	
		#initialization
		for vertex in range(0,26):
			if self.adjacent(src, vertex) :
				distance[vertex]=self.matrix[src][vertex]
				predecessors[vertex]=src
			else:
				distance[vertex]=10000
		
		# looping..until all nodes in confirmed
		w=src
		while confirmed != q:
			#find minimum distance vector
			min_distance=10000000
			keys=distance.keys()
			random.shuffle(keys)
		
			for key, value in predecessors.items():
				if distance[key]<min_distance and key not in confirmed:
					min_distance=distance[key]
					w=key
			confirmed.add(w)

			#compare min_dist
			for vertex in range(0,26):
				if self.adjacent(w, vertex) and vertex not in confirmed:
					if distance[w] + self.matrix[w][vertex] < distance[vertex]:
						distance[vertex]= distance[w] + self.matrix[w][vertex]
						predecessors[vertex]= w
		return predecessors
		
	def Least_Load_Path(self, src, dest):
		global vc_no, timeg_lock
		distance={}
		predecessors={}
		confirmed=set()
		confirmed.add(src)
		q=vc_no.vlist.copy()
		#initialization
		
		for vertex in range(0,26):
			if vc_no.adjacent(src, vertex) :
				w= self.matrix[src][vertex]
				y= vc_no.matrix[src][vertex]*1.0
				x=w/y
				distance[vertex]= x
				predecessors[vertex]=src
			else:
				distance[vertex]=100000
			
		# looping..until all nodes in confirmed
		w=src
		while confirmed != q:
			#find minimum distance vector
			
			min_load=1.1
			keys=distance.keys()
			random.shuffle(keys)
		
			for key, value in predecessors.items():
				if distance[key]<min_load and key not in confirmed:
					min_load=distance[key]
					w=key
			confirmed.add(w)
			

			#compare min_dist
			for vertex in range(0,26):
				if vc_no.adjacent(w, vertex) and vertex not in confirmed:
					
					cur_load=self.matrix[w][vertex]
					max_load=vc_no.matrix[w][vertex]
					load= cur_load/(max_load*1.0)
					a=max(distance[w], load)
					
					if predecessors.has_key(vertex):
						if distance[vertex] > a:
							predecessors[vertex]= w
							distance[vertex]= a
					else:
						predecessors[vertex]= w
						distance[vertex]= a
		return predecessors
				

def readfile_topology(graph, file, switch):
	with open(file) as f:
		for line in f:
			line=line.rstrip().split()
			src=ord(line[0])-65
			dest=ord(line[1])-65
			delay=int(line[2])
			vc_no=int(line[3])
			if switch==1:
				weight=1
			if switch==2:
				weight=delay
			if switch==3:
				weight=vc_no
			graph.insertEdge(src, dest, weight)		
			
def readfile_circuit(scheme, file, switch, packet_rate):
	global total_request, success_request, total_packets, success_no, blocked_no, avg_hop, avg_delay, time_out
	
	with open(file) as f:
		for line in f:
			total_request+=1
			time_stamp, source, dest, duration, end_time= parse(line)
			no_packets= int(packet_rate * duration)
			total_packets+=no_packets
			#remove_expired_virtual_circuit
			remove_vc(time_stamp)

			#shortest path finding by routing_scheme
			if switch == 1 or switch == 2:
				pred= scheme.Dijkstra(source, dest) #path is a reverse path ex: 5->4->0
			else:
				pred= scheme.Least_Load_Path(source, dest) #path is a reverse path ex: 5->4->0
			path, hop_no, prop_no = single_stat(pred, source, dest)
			
		    # add virtual_circuit
			if add_vc(path):
				blocked_no+= no_packets
			else:
				success_request+=1
				success_no+= no_packets
				avg_hop+= hop_no
				avg_delay+=prop_no 
				time_out[end_time]= path
				
def readfile_packet(scheme, file, packet_rate, switch):
	time_list=[]
	
	with open(file) as f:
		for line in f:
			time_stamp, source, dest, duration, end_time= parse(line)
			no_packets= int(packet_rate * duration)
			interval =1.0/packet_rate
			time_stamp=time_stamp
			interval_time=[(interval * x) +time_stamp for x in range(0, no_packets)]
			for i in interval_time:
				time_list.append([i, i+interval, source, dest])
	time_list=	sorted(time_list, key=operator.itemgetter(0))
	
	global start
	start=time.time()
	
	for i in time_list:
		times=i[0]
		while time.time()*10- start < times:
			t=0
		single_packet(scheme, switch, i[2], i[3], i[0], i[1])

def single_packet(scheme, switch, source, dest, packet_time, end_time):
	
	#print "sub-threading", time.time()-start, packet_time
	global total_packets, blocked_no, success_no, total_request, stat_lock, avg_hop, avg_delay, timeg_lock, timeout_lock
	stat_lock.acquire()
	total_packets+=1
	total_request+=1
	stat_lock.release()
	
	remove_vc(packet_time)
	
	
	timeg_lock.acquire()
	if switch == 1 or switch == 2:
		pred= scheme.Dijkstra(source, dest) #path is a reverse path ex: 5->4->0
	else:
		pred= scheme.Least_Load_Path(source, dest) #path is a reverse path ex: 5->4->0
	path, hop_no, prop_no = single_stat(pred, source, dest)
	timeg_lock.release()
	
		# add virtual_circuit
	if add_vc(path):
		stat_lock.acquire()
		blocked_no+=1
		stat_lock.release()
	else:
		stat_lock.acquire()
		success_no+=1
		avg_hop+= hop_no
		avg_delay+=prop_no
		stat_lock.release()
		timeout_lock.acquire()
		time_out[end_time]= path
		timeout_lock.release()
	return
		
def single_stat(pred, src, dest):
	#statistics computation for single circuit
	global delay
	path=[dest]
	while dest!=src:
		dest= pred[dest]				
		path.append(dest)
	
	prop_delay=0
	hop_no= len(path)-1
	for v in range(0, len(path)-1):
		prop_delay+= delay.matrix[path[v]][path[v+1]]
	return path, hop_no, prop_delay

			
def parse(line):
	line=line.rstrip()
	line=line.split()
	time_stamp=float(line[0])
	source=ord(line[1])-65
	dest=ord(line[2])-65
	duration= float(line[3])
	end_time=time_stamp+duration
	return time_stamp, source, dest, duration, end_time
	
def remove_vc(time_stamp):

	
	global time_out, timeg, timeg_lock, timeout_lock
	timeg_lock.acquire()
	timeout_lock.acquire()
	
	for key, expire_path in time_out.items():
		if key<= time_stamp:
			
			for i in range(0, len(expire_path)-1):
				timeg.substract(expire_path[i], expire_path[i+1])
			time_out.pop(key,None)
			
	timeg_lock.release()
	timeout_lock.release()
		
			
def add_vc(path):
	global vc_no, timeg, timeg_lock
	timeg_lock.acquire()
	for v in range(0,len(path)-1):
		if vc_no.matrix[path[v]][path[v+1]]<= timeg.matrix[path[v]][path[v+1]]:
			timeg_lock.release()
			return 1
		
	source=path[0]
	
	for dest in path[1:]:
		timeg.add(source, dest)
		source=dest	
		
	timeg_lock.release()
	return 0
	


def main():
	network_scheme= sys.argv[1];
	routing_scheme= sys.argv[2];
	topo_file=sys.argv[3];
	work_file= sys.argv[4];
	packet_rate=int(sys.argv[5]);
	
	global total_request, total_packets, success_request, blocked_no, success_no, avg_hop, avg_delay
	global time_out, start
	global timeg_lock, timeout_lock, stat_lock
	global delay, vc_no, timeg
	
	stat_lock=threading.Lock()
	timeg_lock=threading.Lock()
	timeout_lock=threading.Lock()
	total_request=0     #total_no of connection request
	total_packets=0
	success_request=0
	blocked_no=0   # blocked packets
	success_no=0   #successfully routed packets
	avg_hop=0      #average hop number
	avg_delay=0     #average propogational delay
	time_out={};   #time_out route dictionary
	
	vc_no= Graph(26)
	delay= Graph(26)
	hop= Graph(26)
	timeg=Graph(26)
	
	readfile_topology(vc_no, topo_file, 3)
	readfile_topology(delay, topo_file, 2)
	readfile_topology(hop, topo_file, 1)
	
	if network_scheme == "PACKET":
		if routing_scheme == "SHP":
			readfile_packet(hop, work_file, packet_rate, 1)
		elif routing_scheme == "SDP":
			readfile_packet(delay, work_file, packet_rate, 2)
		else:
			readfile_packet(timeg, work_file, packet_rate, 3)
		#print time.time()-start
		time.sleep(10)
	

	elif network_scheme == "CIRCUIT":
		if routing_scheme=="SHP":
			readfile_circuit(hop, work_file,1, packet_rate)
		elif routing_scheme=="SDP":
			readfile_circuit(delay, work_file, 2, packet_rate)
		elif routing_scheme=="LLP":
			readfile_circuit(timeg, work_file,  3, packet_rate)
		else:
			print("Invalid routing scheme, choose among SHP, SDP and LLP")
			exit(1)

	else:
		print("Invalid network scheme, choose between PACKET or CIRCUIT")
		exit(1)
	
	print "total number of virtual connection requests: ", total_request
	print " "
	print "total number of packets: ", total_packets
	print " "
	print "number of successfully routed packets: ", success_no
	print" "
	print "percentage of successfully routed packets: ", round(success_no/(total_packets*1.0) *100, 2)
	print" "
	print "number of blocked packets: ", blocked_no
	print" "
	print "percentage of blocked packets: ", round(blocked_no/(total_packets*1.0) *100, 2)
	print" "
	if network_scheme=="CIRCUIT":
		print "average number of hops per circuit: ", round(avg_hop/(success_request*1.0), 2)
		print" "
		print "average cumulative propogation delay per circuit: ", round(avg_delay/(success_request*1.0),2)
	else:
		print "average number of hops per circuit: ", round(avg_hop/(success_no*1.0), 2)
		print" "
		print "average cumulative propogation delay per circuit: ", round(avg_delay/(success_no*1.0),2)
	

if __name__== "__main__":
	main()
