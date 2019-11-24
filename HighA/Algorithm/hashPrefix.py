lstId = 0
prefixes = [[0, 'NAN'] for i in range(135421)]


def getId(txt):
    n = 0
    for i in range(3):
        if i+1==len(txt):
            break
        n += ord(txt[i]) * (10 ** (i + 1))
    return n

with open("files/BigMonster.txt", "r") as f:
    lines = f.readlines()

for l in lines:
    words = l.split()
    for w in words:
        w.lower()
        prefixes[getId(w)][0] += 1
        prefixes[getId(w)][1] = w[:3]

prefixes = sorted(prefixes)
n = int(input('n='))
for i in range(n):
    print(prefixes[-i-1][1])