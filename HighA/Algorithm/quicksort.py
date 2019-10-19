# mergesort
from random import randint
lis = []
for i in range(5000):
	lis.append(randint(0,100))

def quick_one(lis):
	"""
		the first item of the list is the key, all items that are less than the key will be on the left of the key, 
		all items that are larger will be on the right of the key, returns the list and the index of the key.
	"""
	nList = lis.copy()
	key  = lis[0]
	keyI = 0
	pMin = 0
	pMax = len(lis)-1
	while(pMin!=pMax):
		while pMax>keyI:
			if nList[pMax]<=key:
				nList[pMax],nList[keyI] = nList[keyI],nList[pMax]
				keyI = pMax
				break
			pMax-=1
		while pMin<keyI:
			if nList[pMin]>key:
				nList[pMin],nList[keyI] = nList[keyI],nList[pMin]
				keyI = pMin
				break
			pMin+=1
	return nList,keyI

def quick_sort(lis):
	"""
		quick sort with recursion
	"""
	nLis = lis.copy()
	if len(lis) <= 1:
		return lis
	else:
		nLis,keyI = quick_one(nLis)
		return quick_sort(nLis[:keyI])+[nLis[keyI]]+quick_sort(nLis[keyI+1:])

print(lis)
nlis = quick_sort(lis)
print(nlis)