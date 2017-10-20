import os
import sys
from sys import exit
from sys import argv
from collections import defaultdict
import math
from math import sqrt
import copy

latex_switch=False

if sys.argv[1]=='-print':
	latex_switch=True
	raw_file=sys.argv[3]
else:
	raw_file=sys.argv[2]


### process raw data from txt file
def nonblank(f):
	for l in f:
		line=l.strip()
		if line:
			yield line

def display_grid():
	print('\n'.join([''.join(['{:3}'.format(item) for item in row])
		for row in grid]))

rgrid=[]
with open(raw_file,'r') as f:
	for i in nonblank(f): 
		line=[]
		for j in i:
			if j=='\n' or j==' ':
				continue
	
			else:
				line.append(int(j))
		rgrid.append(line)


dimi=0
for i in rgrid:
	dimi+=1

dimj=0
for i in rgrid[0]:
	dimj+=1

if dimi>50 or dimj>50 or dimi<2 or dimj<2:
	print('Incorrect input.')
	sys.exit()

grid=[]
for i in range (dimi+2):
	newl=[]
	if i==0 or i==dimi+1:
		grid.append([0]*(dimj+2))
		continue
	for j in range (dimj+2):
		if j==0 or j==dimj+1:
			newl.append(0)
		else:
			newl.append(rgrid[i-1][j-1])
	grid.append(newl)

for i in range(1,dimi+1):
	for j in range(1,dimj+1):
		if grid[i][j] not in [0,1]:
			print('Incorrect input.')
			sys.exit()

### recursion to get polygon
def direction_sequence(diri):
	if diri==3:
		direction_sequence=[8, 1, 2, 3, 4, 5, 6, 7]
	if diri==4:
		direction_sequence=[1, 2, 3, 4, 5, 6, 7,8]
	if diri==5:
		direction_sequence=[2, 3, 4, 5, 6, 7, 8, 1]
	if diri==6:
		direction_sequence=[3, 4, 5, 6, 7, 8, 1, 2]
	if diri==7:
		direction_sequence=[4, 5, 6, 7, 8, 1, 2, 3]
	if diri==8:
		direction_sequence=[5, 6, 7, 8, 1, 2, 3, 4]
	if diri==1:
		direction_sequence=[6, 7, 8, 1, 2, 3, 4, 5]
	if diri==2:
		direction_sequence=[7, 8, 1, 2, 3, 4, 5, 6]
	return direction_sequence


def g(i,direction):
		if direction==1 or direction==2 or direction==8:
			i=i-1
		if direction==3 or direction==7:
			i=i
		if direction==4 or direction==5 or direction==6:
			i=i+1
		return i
	
def h(j, direction):
		if direction==1 or direction==5:
			j=j
		if direction==2 or direction==3 or direction==4:
			j=j+1
		if direction==6 or direction==7 or direction==8:
			j=j-1
		return j

		
cd=defaultdict(list)
area=defaultdict(list)

def get_poly(i0, j0, i, j, direction, grid, count):
	## use default dictionary to record each direction to be used to calculate perimeter, area and convex
	cd[count].append(direction)
	temp=(i,j)
	area[count].append(temp)

	##base case stop when find polygon
	if i==i0 and j==j0:
		grid[i][j]=count
		return True
	
	##base case when hit deadend
	if grid[i][j]!=1:
		return False

	##recursive calls, first test with same direction, then if fails, change direction by get_1_poly
	diri=direction
	grid[i0][j0]=1
	grid[i][j]=count

	for direction in direction_sequence(diri):
	
			tempi=g(i,direction)
			tempj=h(j,direction)
			if grid[tempi][tempj]==1:
				if get_poly(i0, j0, tempi, tempj, direction, grid, count):
					return True
				else:
					continue
				
			if direction==direction_sequence(diri)[-1]:
				for k,v in cd.items():
					if k==count:
						v.pop()
				for k,v in area.items():
					if k==count:
						v.pop()
				grid[i][j]=1		
	return False
	
### main function to dye the grid into different polygon color(number)			

for count in (2,3):
	for i in range(1,dimi+1):
		for j in range(1,dimj+1):
			if grid[i][j]==1:
				grid[i][j]=count
				for direction in direction_sequence(3):
					i1=g(i,direction)
					j1=h(j, direction)
					if grid[i1][j1]==1:
						break
		
				if get_poly(i,j,i1,j1,direction, grid,count):
					count+=1
				else:
					grid[i][j]=1
			

###exit if cannot get polygon
for i in range(1,dimi+1):
	for j in range(1,dimj+1):
		if grid[i][j]==1:
			print('Cannot get polygons as expected.')
			sys.exit()


cd=dict(cd)
ap=defaultdict(list)
areacopy=copy.deepcopy(area)


### find perimeter and convex by processsing the dictionary CD from the grid recursion
for k in cd:
	straight=0
	diagonal=0
	convex='yes'
	for v in range (0,len(cd[k])):
		##perimeter
		if cd[k][v]==1 or cd[k][v]==3 or cd[k][v]==5 or cd[k][v]==7:
			straight+=1
		else:
			diagonal+=1
	

		##convex
		if (cd[k][v-1]==1 and (cd[k][v]==6 or cd[k][v]==7 or cd[k][v]==8) ) or (cd[k][v-1]==2 and (cd[k][v]==1 or cd[k][v]==7 or cd[k][v]==8) ) or (cd[k][v-1]==3 and (cd[k][v]==1 or cd[k][v]==2 or cd[k][v]==8) ) or (cd[k][v-1]==4 and (cd[k][v]==1 or cd[k][v]==2 or cd[k][v]==3) ) or (cd[k][v-1]==5 and (cd[k][v]==4 or cd[k][v]==2 or cd[k][v]==3) ) or (cd[k][v-1]==6 and (cd[k][v]==4 or cd[k][v]==5 or cd[k][v]==3) ) or (cd[k][v-1]==7 and (cd[k][v]==4 or cd[k][v]==5 or cd[k][v]==6) ) or (cd[k][v-1]==8 and (cd[k][v]==5 or cd[k][v]==6 or cd[k][v]==7) ):
			convex='no'
			
	ap[k].append(straight)
	ap[k].append(diagonal)
	ap[k].append(convex)

###find the rotate polygon
def rotate(poly,tta, cp):
	transform = []
	for i in poly :
		transform.append(rpoint (cp, i, tta)) 
	return transform

### find the rotated position from center point
def rpoint(cp ,point,tta):
	rad_angle = math.radians(tta)
	temp = point[0]-cp[0] , point[1]-cp[1]
	temp = [ temp[0]*math.cos(rad_angle)-temp[1]*math.sin(rad_angle) , temp[0]*math.sin(rad_angle)+temp[1]*math.cos(rad_angle)]
	temp = [round(temp[0]+cp[0], 1), round(temp[1]+cp[1], 1)]
	return temp


### find area and nb_invariant rotation by processsing the dictionary area from the grid recursion
for k in area:
	a=0
	for v in range(0, len(area[k])):
		if v==0:
			plus0= area[k][0][0] * area[k][1][1]
			minus0= area[k][0][0]*area[k][-1][1]
			a=a+plus0-minus0
			continue

		if v==len(area[k])-1:
			plus1=area[k][-1][0] * area[k][0][1]
			minus1=area[k][-1][0]*area[k][v-1][1]
			a=a+plus1-minus1
			break

		plus= area[k][v][0] * area[k][v+1][1]
		minus= area[k][v][0]*area[k][v-1][1]
		a=a+plus-minus

	aa=round(a*0.5)
	a=round(0.4*0.4*0.5*-a,2)
	
	
	ap[k].append(a)
	
	##finding nb of rotation by calculating centroid of each polygon
	imax=len(area[k])-1
	c_x=0
	c_y=0
	for i in range(0, imax):

		c_x += (area[k][i][0]+ area[k][i+1][0])* ((area[k][i][0]*area[k][i+1][1])-(area[k][i+1][0]*area[k][i][1]))
		c_y += (area[k][i][1]+ area[k][i+1][1])* ((area[k][i][0]*area[k][i+1][1])-(area[k][i+1][0]*area[k][i][1]))
	c_x += (area[k][imax][0]+ area[k][0][0])* ((area[k][imax][0]*area[k][0][1])-(area[k][0][0]*area[k][imax][1]))
	c_y += (area[k][imax][1]+ area[k][0][1])* ((area[k][imax][0]*area[k][0][1])-(area[k][0][0]*area[k][imax][1]))
	try:
		c_x /= (aa*6.0)
	except:
		c_x=0
	try:
		c_y /= (aa*6.0)
	except:	
		c_y=0
	## finding rotation each 45 degree on the centroid point from 0 to 360
	residuex=  c_x- int(c_x)
	residuey= c_y-int(c_y)
	center_point=(c_x, c_y)

	if (residuex==0.5 or residuex==0) and  (residuey==0.5 or residuey==0):
		rotation=0
		for theta in [0, 45, 90, 135, 180, 225, 270, 315]:
			new_list=rotate(area[k],theta, center_point)

			area[k]=[[float(y) for y in x] for x in area[k]]
			new_list.sort()
			area[k].sort()
			
			if new_list==area[k]:
				rotation+=1
		ap[k].append(rotation)
	else:
		ap[k].append(1)

	### finding depth 
	depth=0
	if k==2:
		ap[k].append(depth)
		continue
	for i in range(2,k):
		count=0
		index=0
		for j in range(len(area[k])):
			j=areacopy[k][j]
			ji=j[0]
			jj=j[1]
			marker=0
			# up
			index+=1
			for up in range(0, ji):
				x= (up, jj)
				if x in areacopy[i]:
					marker+=1
					break
				
			for down in range(ji, dimi+2):
				x=(down, jj)
				if x in areacopy[i]:
					marker+=1
					break
				
			for left in range(0, jj):
				x=(ji, left)
				if x in areacopy[i]:
					marker+=1
					break

			for right in range(jj, dimj+2):
				x=(ji, right)
				if x in areacopy[i]:
					marker+=1
					break
			
			if marker==4:
				count+=1
		if count==index:
			depth+=1
	ap[k].append(depth)

depth_list=[]
area_list=[]
##### txt file
for i in ap:
	peris= round(ap[i][0]*0.4, 2)
	perid= ap[i][1]
	convex=ap[i][2]
	area=ap[i][3]
	nbr=ap[i][4]
	depth=ap[i][5]
	depth_list.append(depth)
	area_list.append(area)
	if not latex_switch:
		print(f'Polygon {i-1}:')
		if perid==0:
			print('    Perimeter:', peris)
		elif peris==0:
			print(f'    Perimeter: {perid}*sqrt(.32)')
		else:
			print(f'    Perimeter: {peris} + {perid}*sqrt(.32)')
		print('    Area:', format(area, '.2f'))
		print('    Convex:', convex)
		print('    Nb of invariant rotations:', nbr)
		print('    Depth:', depth)

#### process data for latex into a dictionary contain all the info for latex
codinate=defaultdict(list)
for i in cd:
	codinate[i].append(areacopy[i][-1])
	for j in range(0,len(cd[i])-1):
		if cd[i][j+1] - cd[i][j]!=0:
			codinate[i].append(areacopy[i][j])

new_c=defaultdict(list)
for i in codinate:
	for j in range(0, len(codinate[i])):
		y=codinate[i][j][0]
		x=codinate[i][j][1]
		new_y= y-1
		new_x= x-1
		new_codinate=(new_x, new_y)
		new_c[i].append(new_codinate)
	
init_bound=[(0, 0), (dimj-1, 0), (dimj-1, dimi-1), (0, dimi-1)]

max_depth=max(depth_list)
max_area=max(area_list)
min_area=min(area_list)
latex=defaultdict(list)
for i in range(max_depth+1):
	for j in ap:
		ap_depth=ap[j][5]
		ap_area= ap[j][3]
		if ap_depth==i:
			filler= int(round((max_area- ap_area)/ (max_area- min_area) *100, 0))
			latex[i].append([filler, new_c[j]])
			
#### #########################################################
## ascii tex file

from argparse import ArgumentParser
from re import sub
from itertools import count
import os

if latex_switch:
	parser = ArgumentParser()
	parser.add_argument('-print', '--dynamic', action= 'store_true')
	parser.add_argument('--file', dest = 'txt_filename', required = True)
	args = parser.parse_args()

	txt_filename = args.txt_filename

	txt_name = sub('\..*$', '', txt_filename)
	ascii_txt_name = txt_name
	tex_filename = ascii_txt_name + '.tex'

	with open(tex_filename, 'w') as tex_file:
		print('\\documentclass[10pt]{article}\n'
			'\\usepackage{tikz}\n'
			'\\usepackage[margin=0cm]{geometry}\n'
			'\\pagestyle{empty}\n'
			'\n'
			'\\begin{document}\n'
			'\n'
			'\\vspace*{\\fill}\n'
			'\\begin{center}\n'
			'\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]', file=tex_file)
		
		print('\\draw[ultra thick]', end=' ', file=tex_file)
		for i in range(len(init_bound)):
			print(init_bound[i], '--', end=' ', file=tex_file)
		print('cycle;', file=tex_file)
    ################################################################################################333333
		for i in latex:
			print('%Depth', i, file=tex_file)
			for j in range(len(latex[i])):
				print(f'\\filldraw[fill=orange!{latex[i][j][0]}!yellow]', end=' ', file=tex_file)
				for k in range(len(latex[i][j][1])):
					print(latex[i][j][1][k],  '--',end=' ', file=tex_file)
				print('cycle;', file=tex_file)
		
######################################################################################################33
		print('\\end{tikzpicture}\n'
			'\\end{center}\n'
			'\\vspace*{\\fill}\n'
			'\n'
			'\\end{document}', file = tex_file)

	os.system('pdflatex ' + tex_filename)
	for file in (ascii_txt_name + ext for ext in ('.aux', '.log')):
		os.remove(file)

