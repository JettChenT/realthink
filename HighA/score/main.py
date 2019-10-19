from random import randint,random
import time
nList = [i for i in range(5000)]

def caladd():
	n = 0
	for i in range(50000000):
		n+=5
	# print(n)
	return

def floatadd():
	n = 0
	for i in range(50000000):
		n+=0.2
	return

def addminus():
	n = 1
	for i in range(2,50000000):
		if i%2==0:
			n+=1/i
		else:
			n-=1/i

def bubble():
	global nList
	for i in range(len(nList)):
		for j in range(i,len(nList)):
			if nList[i]<nList[j]:
				nList[i],nList[j] = nList[j],nList[i]
	return

def bubble2():
	global nList
	for i in range(len(nList)):
		for j in range(i,len(nList)):
			if nList[i]>nList[j]:
				nList[i],nList[j] = nList[j],nList[i]
	return

def count_score(fun):
	st = time.time()
	fun()
	et = time.time()
	print(10000//(et-st))

count_score(caladd)
count_score(floatadd)
count_score(bubble)
count_score(bubble2)
count_score(addminus)