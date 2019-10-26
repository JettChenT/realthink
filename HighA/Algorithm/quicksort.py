# mergesort
from random import randint
lis = []
for i in range(100):
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

def quick_onePy(lis):
	"""python styled quick one"""
	key = lis[0]
	smLis = []
	bgLis = []
	for n in lis[1:]:
		if n<=key:
			smLis.append(n)
		else:
			bgLis.append(n)
	return smLis+[key]+bgLis,len(smLis)

def quick_sortPy(lis):
	"""
		quick sort with recursion, python styled
	"""
	nLis = lis.copy()
	if len(lis) <= 1:
		return lis
	else:
		nLis,keyI = quick_onePy(nLis)
		return quick_sort(nLis[:keyI])+[nLis[keyI]]+quick_sort(nLis[keyI+1:])

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

def quick_oneNR(lis,pMin,keyI,pMax):
	nList = lis.copy()
	key  = lis[keyI]
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

def quick_sortNR(lis):
	"""quick sort without recursion"""
	mem = [(0,0,len(lis)-1)]
	c = 1
	while len(mem)!=0:
		p = 0
		# print(c)
		c+=1
		# print(mem[p])
		lis,keyI = quick_oneNR(lis,mem[p][0],mem[p][0],mem[p][2])
		if len(lis) == 0:
			# print("break")
			break
		else:
			if (keyI-1)-mem[p][0]>0:
				mem.append((mem[p][0],mem[p][0],keyI-1))
			if (mem[p][-1])-(keyI+1)>0:
				mem.append((keyI+1,keyI+1,mem[p][-1]))
		mem.pop(p)
		# print("ed")
	# print("out of while loop")
	return lis
# print(lis)
nlis = quick_sortNR(lis)
print("done")
print(nlis)
if nlis==sorted(lis):
	print("YAY!")