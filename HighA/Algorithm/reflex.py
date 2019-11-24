nodeList = []
source = '/Users/jettchen/anaconda3'
class CLS_node(object):
    def __init__(self,v,i,l,r):
        self.left = l
        self.right = r
        self.ind = i
        self.value = v
    def __str__(self):
        return str(nodeList[self.left])+str(self.value)+str(nodeList[self.right])
