import string
from OP import OP

def three_part(A):
    q = A[0]
    l = []
    r = []
    for i in A[1:]:
        if i > q:
            r.append(i)
        if i < q:
            l.append(i)
    return l + [q] * A.count(q) + r

f = OP('rosalind_par3.txt')
input = f.i()
n = input.readline()
A = list(map(int, input.readline().split()))

ans = ' '.join(list(map(str, three_part(A))))
f.o(ans)