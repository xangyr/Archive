import string
import OP
from merge import merge

def ms(A, n):
    if n < 2:
        return A
    mid = round(n/2)
    L = ms(A[:mid], len(A[:mid]))
    R = ms(A[mid:], len(A[mid:]))
    return merge(L,R)

f = OP.OP('rosalind_ms.txt')
input = f.i()
n = int(input.readline().split()[0])
A = list(map(int, input.readline().split()))
ans = ' '.join(list(map(str, ms(A, n))))
f.o(ans)
