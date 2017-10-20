
import os.path
import sys
from collections import deque


text=input("Please enter the name of the file you want to get data from: ")

try:
	fsock = open(text,'r')
except IOError:
	print('Sorry, there is no such file.')
	sys.exit()
		
		
try:
	lines = filter(None, (line.rstrip() for line in open(text)))
	n=0
	c=0
	list = [[] for _ in range(2)]	
	for line in lines:
		c+=1
		if c>len(list):
			raise ValueError
		line=line.split()
		print (line)
		for i in line:
			i=int(i)
			list[n].append(i)
		n+=1

	upper=list[0]
	lower=list[1]

	if len(upper)!=len(lower):
			raise ValueError
	if len(upper)<2  or len(lower) < 2:
			raise ValueError
	
	for i, j in zip(upper, lower):
		if i<=j:
			raise ValueError

except ValueError:
	print('Sorry, input file does not store valid data.')
	sys.exit()

	
###convert elements from string into integers in list	
upper = [int(i) for i in upper]
lower = [int(i) for i in lower]

###find the maximum visible distance from entrance
def extrance():
	d=collections.deque()
	d.extend(upper[0])
	d.extend(lower[0])
	distance=0
	for i , j in zip(range(1,len(upper)), range(1,len(lower))):
		if upper[i] < d[0]:
			d.popleft
			d.extendleft(i)
		if lower[j] > d[1]:
			d.pop()
			d.extend(j)
		distance+=1
		if d[0]==d[1]:
			return distance
			
		
###find the maximum visible distance inside the tunnel		
def maxdistance():
	max_distance=0
	
	u=1
	temp=0
	for i , j in zip(range(1,len(upper)), range(1,len(lower))):
		ceiling=min(upper[u:i+1])
		floor=max(lower[u:j+1])
		if upper[j] <=floor or lower[j]>=ceiling or i==len(upper)-1:
			if i==len(upper)-1:
				temp=i-u+1
			else:
				temp=i- u
			if temp>max_distance:
				max_distance=temp
				maximum=0
				minimum=0
				u=i+1
	return max_distance
		
print('From the west, one can into the tunnel over a distance of', extrance())
print('Inside the tunnel, one can into the tunnel over a maximum distance of', maxdistance())


