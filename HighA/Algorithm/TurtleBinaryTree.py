import turtle
class CLS_tree():
    """
    The binary tree
    """
    DEG = 30
    def __init__(self,r):
        self.root = r
        self.widLst = [0 for _ in range(self.dep(self.root))]

    def sortInsert(self,node,start):
        return
    def dep(self,start,dept=1):
        if start == None:
            return dept
        ld = self.dep(start.left,dept+1)
        rd = self.dep(start.right,dept+1)
        if ld>rd:
            return ld
        else:
            return rd
    def wid(self,start,dept=0):
        if(dept==0):
            self.widLst = [0 for _ in range(self.dep(self.root))]
        if start == None:
            return
        self.widLst[dept]+=1
        ld = self.wid(start.left,dept+1)
        rd = self.wid(start.right,dept+1)
        return max(self.widLst)
    def draw(self,tt,start){
        
    }
    def __repr__(self):
        return str(self.root)


class CLS_node():
    """
    A Node in binary tree
    """
    def __init__(self,v,l,r):
        self.value = v
        self.left = l
        self.right = r
    def __str__(self):
        if self.left == None and self.right == None:
            return str(self.value)
        elif self.left == None:
            return str(self.value)+str(self.right)
        elif self.right == None:
            return str(self.left)+str(self.value)
        else:
            return str(self.left)+str(self.value)+str(self.right)
    def get_child(self):
        if self.left == None and self.right == None:
            return [None,None]
        elif self.left == None:
            return [None,self.right]
        elif self.right == None:
            return [self.left,None]
        else:
            return [self.left,self.right]

root = CLS_node('o',None,None)
tree = CLS_tree(root)
strst = set('tzlhpfybd')
for s in strst:
    node = CLS_node(s,None,None)
    tree.sortInsert(node,tree.root)
