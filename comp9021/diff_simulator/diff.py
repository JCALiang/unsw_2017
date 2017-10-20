##Aissigment 3
import re
from collections import defaultdict


class DiffCommands:
	def __init__(self, file):
		file_object=open(file)
		d=defaultdict(list)
		dd=defaultdict(list)
		ddd=defaultdict(list)
	
		for counter, i in enumerate(file_object, start=1):
			if not re.match('^(\d+)(?:,(\d+))?d(\d+)\n$|^(\d+)a(\d+)(?:,(\d+))?\n$|^(\d+)(?:,(\d+))?c(\d+)(?:,(\d+))?\n$' , i):
				raise DiffCommandsError()

			m=re.match('^(\d+)(?:,(\d+))?d(\d+)\n$|^(\d+)a(\d+)(?:,(\d+))?\n$|^(\d+)(?:,(\d+))?c(\d+)(?:,(\d+))?\n$' , i)
			
			if m.group(3) and m.group(1):
				if counter==1 and int(m.group(3))+1 > int(m.group(1)):
					raise DiffCommandsError()


			for j in range(11):
				ddd[counter].append(m.group(j))
		
			
			
			if counter>1 and m.group(7) is not None and m.group(9) is not None and ddd[counter-1][3] is not None and ddd[counter-1][1] is not None and m.group(8) is None and m.group(10) is None:
				if ddd[counter-1][2] is not None:
					if (int(m.group(9))- (int(ddd[counter-1][3])+1) < int(m.group(7))- int(ddd[counter-1][2])):
						raise DiffCommandsError()
				else: 
					if (int(m.group(9))- (int(ddd[counter-1][3])+1) < int(m.group(7))- int(ddd[counter-1][1])):
						print(i)
						raise DiffCommandsError()
			

			for j in range(11):
				dd[i].append(m.group(j))

			###delete
			if m.group(1) and m.group(2):
				for x in range(int(m.group(1)), int(m.group(2))+1):
					d['del'].append(x-1)
				
			elif m.group(1):
				d['del'].append(int(m.group(1))-1)
		
			##add
			if m.group(5) and m.group(6):
				for x in range(int(m.group(5)), int(m.group(6))+1):
					d['add'].append(x-1)
			elif m.group(5):
				d['add'].append(int(m.group(5))-1)
		
				
			###change file 1

			if m.group(7) and m.group(8):
				for x in range(int(m.group(7)), int(m.group(8))+1):
					d['cha1'].append(x-1)
			elif m.group(7):
				d['cha1'].append(int(m.group(7))-1)
			
			
			###change file 2

			if m.group(9) and m.group(10):
				for x in range(int(m.group(9)), int(m.group(10))+1):
					d['cha2'].append(x-1)
			elif m.group(9):
				d['cha2'].append(int(m.group(9))-1)
			
	
		self.file=file
		self.d=d
		self.dd=dd

	def __len__(self):
		file_object=open(self.file)
		length=0
		for i in file_object:
			length+=1
		return length

	def __str__(self):
		file_object=open(self.file)
		newstr=''
		count=1
		for i in file_object:
			if count== len(self):
				newstr+=i.rstrip('\n')
			else:
				newstr+=i
			count+=1
		return newstr

class DiffCommandsError(Exception):
	def __init__(self):
		Exception.__init__(self, 'Cannot possibly be the commands for the diff of two files')


class OriginalNewFiles():
	def __init__(self, x, y):
		str1=''
		str2=''
		for i in open(x):
			str1+=i
		for j in open(y):
			str2+=j
		a=str1.splitlines()
		b=str2.splitlines()
		self.a=a
		self.b=b
	
	def lcs(A, B):
		# create a matrix to store all the LCS
		x=len(A)
		y=len(B)
		matrix = [[0] * (y+1) for _ in range(x+1)]
		for i in range(x-1,-1,-1):
			for j in range(y-1,-1,-1):
				if A[i] == B[j]:
					matrix[i][j] = matrix[i+1][j+1]+1
				else:
					matrix[i][j] = max(matrix[i][j+1], matrix[i+1][j])
		# Step 2: restore sequence from the matrix
		tt=[]
		i=0
		j=0
		while (i < x) and (j < y):
			if A[i] == B[j]:
				tt.append(A[i])
				i+=1
				j+=1
			elif matrix[i+1][j] >= matrix[i][j+1]:
				i+=1
			else:
				j+=1
		return matrix[0][0], tt


	def is_a_possible_diff(self, diffcommand):
		a=self.a
		b=self.b
		self.diffcommand=diffcommand
		remove_key=self.diffcommand.d
		lcs_length, lcs_list= OriginalNewFiles.lcs(a, b)
		after_a=[]
		after_b=[]
		for i in range(len(a)):
			if not (i in remove_key['del'] or i in remove_key['cha1']):
				after_a.append(a[i])
		
		for i in range(len(b)):
			if not (i in remove_key['add'] or i in remove_key['cha2']):
				after_b.append(b[i])	
		
		if len(after_a)!= lcs_length:
			return False
		if len(after_b)!= lcs_length:
			return False
		if len(after_a)!= len(after_b):
			return False
		if after_b!= after_a:
			return False
	
		return True
		
		
	def output_diff(self, diffcommand):
		a=self.a
		b=self.b
		dicta=defaultdict(list)
		dictb=defaultdict(list)

		for i in range(len(a)):
			dicta[i+1].append(a[i])
		for j in range(len(b)):
			dictb[j+1].append(b[j])
			
		self.diffcommand=diffcommand
		key=self.diffcommand.dd
		for i in open(self.diffcommand.file):
			print(i.rstrip('\n'))
			if key[i][1] and key[i][2]:
				for x in range(int(key[i][1]), int(key[i][2])+1):
					print ('<', ', '.join(dicta[x]))
			elif key[i][1]:
				print ('<', ', '.join(dicta[int(key[i][1])]))

			if key[i][5] and key[i][6]:
				for x in range(int(key[i][5]), int(key[i][6])+1):
					print ('>', ', '.join(dictb[x]))
			elif key[i][5]:
				print ('>', ', '.join(dictb[int(key[i][5])]))

			if key[i][7] and key[i][8]:
				for x in range(int(key[i][7]), int(key[i][8])+1):
					print ('<', ', '.join(dicta[x]))
			elif key[i][7]:
				print ('<', ', '.join(dicta[int(key[i][7])]))

			if key[i][7] and key[i][9]:
				print('---')

			if key[i][9] and key[i][10]:
				for x in range(int(key[i][9]), int(key[i][10])+1):
					print ('>', ', '.join(dictb[x]))
			elif key[i][9]:
				print ('>', ', '.join(dictb[int(key[i][9])]))


	def output_unmodified_from_original(self, diffcommand):
		a=self.a
		b=self.b
		self.diffcommand=diffcommand
		lcs_length, lcs_list= OriginalNewFiles.lcs(a, b)
		switch=1
		counter=0

		for i in range(len(a)):
			if counter==lcs_length:
				if switch:
					print('...')
				break
			if a[i] != lcs_list[counter]:
				if switch:
					print('...')
					switch=0
				else:
					continue
			else:
				print (a[i])
				counter+=1
				switch=1
				
		
		
	def output_unmodified_from_new(self, diffcommand):
		a=self.a
		b=self.b
		self.diffcommand=diffcommand
		lcs_length, lcs_list= OriginalNewFiles.lcs(a, b)
		switch=1
		counter=0
		for i in range(len(b)):
			if counter==lcs_length:
				if switch:
					print('...')
				break
			if b[i] != lcs_list[counter]:
				if switch:
					print('...')
					switch=0
				else:
					continue
			else:
				print (b[i])
				counter+=1
				switch=1


"""

	def output_unmodified_from_new()
"""
