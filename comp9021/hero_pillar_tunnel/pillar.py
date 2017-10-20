import os.path
import sys
from numpy import diff
from collections import defaultdict


array=[5,9,18,27,30,31,32,36,40,44,54]
	
bool=0
perfect=0
dy=diff(array)/1
dy=list(dy)

def checkEqual2(dy):
	return len(set(dy)) <= 1

if checkEqual2(dy)==True:
	print('The ride is perfect!')
	longest=len(array)-1
	perfect=0
else:
	##longest good ride
	print('The ride could be better...')
	longest=1
	lenmax=1
	for i in range(1,len(dy)):
		if dy[i]== dy[i-1]:
			lenmax+=1
		else:
			if lenmax>longest:
				longest=lenmax
				lenmax=1
			else:
				lenmax=1
				
	###find pillars to remove	
	list=[]
	for i in range(0,len(array)-1):
		gradient=array[i+1]-array[i]
		temp=0
		for j in range(0,len(array)-1):
			if abs(array[j+1]-array[j])>gradient:
				break
			elif abs(array[j+1]-temp)==gradient:
				list.append(gradient)
				temp=0
			elif abs(array[j+1]-array[j])==gradient:
				list.append(gradient)
			else:
				temp=array[j]
				continue
				

	x= max(list,key=list.count)
	
	perfect=0
	for i in array:
		if i%x!=0:
			perfect+=1
	
print('The longest good ride has a length of:',longest)
print('The minimal number of pillars to remove to build a perfect ride from the rest is:', perfect)
	
