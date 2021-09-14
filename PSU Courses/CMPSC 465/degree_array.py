import string
import OP

def da(li, ed):
    ed = list(map(int,ed.split()))
    for i in ed:
        li[i - 1] += 1
    return li
f = OP.OP('rosalind_deg.txt')
input = f.i()

ve = input.readline().split()
v, e = int(ve[0]), int(ve[1])

li = [0 for i in range(v)]

edges = input.readlines()

for ed in edges: ans = da(li, ed)
ans = ' '.join(map(str, ans))
f.o(ans)