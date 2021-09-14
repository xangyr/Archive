from OP import OP
import string

def ps(A, k):
    A.sort()
    return A[:k]

f = OP('rosalind_ps.txt')
input = f.i()

n = input.readline().split()
A = list(map(int, input.readline().split()))
k = int(input.readline().split()[0])

ans = ' '.join(list(map(str, ps(A, k))))
f.o(ans)
