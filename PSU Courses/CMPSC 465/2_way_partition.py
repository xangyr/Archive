import string
from OP import OP

def two_par(A):
    s = A[0]
    l = []
    r = []
    for i in A[1:]:
        if i < s:
            l.append(i)
        if i > s:
            r.append(i)
    return l + [s] + r

f = OP('rosalind_par.txt')
input = f.i()
n = input.readline()
A = list(map(int, input.readline().split()))
ans = ' '.join(list(map(str, two_par(A))))
f.o(ans)