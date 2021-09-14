from OP import OP
import heapq
import string

def hs(A, n):
    heap = []
    for i in range(n):
        heapq.heapify(A)
        heap.append(A.pop(0))
    return heap

f = OP('rosalind_hs.txt')
input = f.i()
n = int(input.readline().split()[0])
A = list(map(int, input.readline().split()))

ans = ' '.join(list(map(str, hs(A, n))))
f.o(ans)
