import os,re
# init
p = 0
source =  '/Users/jettchen/documents'
crtList = os.listdir(source)
target = re.compile(
    r'.*(\.pdf)+$',
    )
mem = []
for pth in crtList:
    tmp = os.path.join(source,pth)
    if os.path.isdir(tmp):
        mem.append(tmp)
while mem:
    cur = mem[p]
    crtList = os.listdir(cur)
    for t in crtList:
        if re.match(target,t) and os.path.isfile(os.path.join(cur,t)):
            print(os.path.join(cur,t))
    for pth in crtList:
        tmp = os.path.join(cur,pth)
        if os.path.isdir(tmp):
            mem.append(tmp)
    del(mem[p])
    