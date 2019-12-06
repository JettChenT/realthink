from PIL import Image 
from pprint import pprint
import math
def get_image(im):
	if type(im) == str:	   
		image = Image.open(im,'r')
	else:
		image = im
	width, height = image.size
	pixel_values = list(image.getdata())
	# if image.mode == 'RGB':
	#	  channels = 3
	# elif image.mode == 'L':
	#	  channels = 1
	# else:
	#	  print("Unknown mode: %s" % image.mode)
	#	  return None
	# # pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
	return pixel_values
def get_size(image_path):
	"""Get a numpy array of an image so that one can access values[x][y]."""
	image = Image.open(image_path, 'r')
	width, height = image.size
	return width,height
def avgCl(lst):
	"""return the average RGB of a RGB list"""
	c1=c2=c3=0
	n = len(lst)
	for c in lst:
		c1+=c[0]
		c2+=c[1]
		c3+=c[2]
	c1,c2,c3=c1/n,c2/n,c3/n
	return [c1,c2,c3]

def dist(x1,y1,z1,x2,y2,z2):
	return math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

def blockDist(block1,block2):
	return dist(block1.avg[0],block1.avg[1],block1.avg[2],block2.avg[0],block2.avg[1],block2.avg[2])

def find(lst,num):
	for i in range(len(lst)):
		if lst[i]==num:
			return i
	return None

def reco(blst,target):
	dislist = []
	for b in blst:
		dislist.append(blockDist(b,target))
	return str(blst[find(dislist,min(dislist))])
class block(object):
	def __init__(self,url,rstr=''):
		self.url = url
		self.pixel_values = get_image(url)
		self.avg = avgCl(self.pixel_values)
		self.rstr = rstr
	def __repr__(self):
		return self.url
	def __str__(self):
		return self.rstr
box = block('./blocks/box.bmp','B')
floor = block('./blocks/floor.bmp','#')
ground = block('./blocks/ground.bmp','=')
ladder = block('./blocks/ladder.bmp','H')
bar = block('./blocks/bar.bmp','-')
police = block('./blocks/lp02.bmp','P')
runner = block('./blocks/lr01.bmp','R')
vground = block('./blocks/vground.bmp','.')
void = block('./blocks/void.bmp',' ')
# test = block('./blocks/test.png')
# print(test)
blockList = [box,floor,ground,ladder,bar,police,runner,vground,void]
# print(reco(blockList,test))
im = Image.open('./blocks/level06.png')
sampleBlock = Image.open('./blocks/floor.bmp')
print(sampleBlock.size)
print(im.size)
nMap = [[0 for n in range(im.size[1]//sampleBlock.size[1])]for _ in range(im.size[0]//sampleBlock.size[0])]
cnt = 0
print(im.size[0]//sampleBlock.size[0])
fout = open('./maps/level06.txt','w')
for y in range(im.size[1]//sampleBlock.size[1]):
	tstr = ''
	for x in range(im.size[0]//sampleBlock.size[0]):
		cnt+=1
		area = (x*sampleBlock.size[0],y*sampleBlock.size[1],x*sampleBlock.size[0]+sampleBlock.size[0],y*sampleBlock.size[1]+sampleBlock.size[1])
		nimg = im.crop(box=area)
		nimg.save('./tmp/block{c}.bmp'.format(c=cnt),'BMP')
		# pprint(get_image(im))
		nBlock = block(nimg)
		# print(cnt)
		# if cnt==34:
		# print(reco(blockList,nBlock),end='')
		tstr+=reco(blockList,nBlock)
	tstr+='\n'
	fout.write(tstr)
fout.close() 