#reference https://docs.python.org/3/library/heapq.html
import heapq
import OP

def build_heap(A):
    #print(A)
    heapq._heapify_max(A)
    return A

f = OP.OP('rosalind_hea.txt')
input = f.i()
n = input.readline()
A = list(map(int, input.readline().split()))
ans = ' '.join(list(map(str, build_heap(A))))
f.o(ans)