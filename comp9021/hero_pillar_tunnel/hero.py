import sys
import copy
import random


power=[random.randint(-100, 100) for x in range(10000)]
flips=1000

print('start')
	
power= list(map(int, power))
once=power[:]
consecutive=power[:]
arbit=power[:]
greatest=copy.copy(power)

###greatest
count=0
while count<flips:
	x=min(greatest)
	greatest.remove(x)
	y=x*-1
	greatest.append(y)
	count+=1
greatest=sum(greatest)

print('Possibly flipping the power of the same hero many times, the greatest achievable power is {}.'.format(greatest))
##maximum once
count=0
temp=[]
while count<flips:
	x=min(once)
	once.remove(x)
	y= x*-1
	temp.append(y)
	count+=1
	
once=once+temp
once=sum(once)	

print('Flipping the power of the same hero at most once, the greatest achievable power is {}.'.format(once))

##consecutive

consecutive_min=consecutive[:]
for i in range(len(consecutive_min)):
	if consecutive_min[i]>0:
		consecutive_min[i]=(-1*consecutive_min[i])
print('start2')
total=sum(consecutive_min)
total2=sum(consecutive_min)

for i in range(0, len(consecutive)+1-flips):
	count=0
	marker=i
	temp=consecutive[:]
	while count<flips:
		temp[marker]=(-1*temp[marker])
		marker+=1
		count+=1
	temp_sum=sum(temp)
	if temp_sum> total:
		total=temp_sum
consecutive=total
print('Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is {}.'.format(consecutive))
	
#arbit
for f in range(0,len(arbit)+1):
	for i in range(0, len(arbit)+1-f):
		count=0
		marker=i
		temp=arbit[:]
		while count<f:
			temp[marker]=(-1*temp[marker])
			marker+=1
			count+=1
		temp_sum=sum(temp)
		if temp_sum> total2:
			total2=temp_sum
			
			
arbit=total2


print('Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is {}.'.format(consecutive))
print('Flipping the power of arbitrarily many consecutive heroes, the greatest achievable power is {}.'.format(arbit))
