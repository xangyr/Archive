import string
from OP import OP

def qs(A):
    if len(A) == 0:
        return A
    l = []
    r = []
    piv = A[0]

    for i in A:
        if i < piv:
            l.append(i)
        else:
            r.append(i)

    return qs(l).extend(qs(r))

f = OP('rosalind_qs.txt')
input = f.i()
n = int(input.readline().split()[0])
A = list(map(int, input.readline().split()))

ans = ' '.join(list(map(str, quicksort(A))))
f.o(ans)
