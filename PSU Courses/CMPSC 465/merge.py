# reference: https://en.wikipedia.org/wiki/Merge_algorithm
import string
import OP

def merge(A, B):
    C = []
    A_i = 0
    B_i = 0
    while A_i < len(A) and B_i < len(B):
        if A[A_i] > B[B_i]:
            C.append(B[B_i])
            B_i += 1
        else:
            C.append(A[A_i])
            A_i += 1
    C.extend(A[A_i:])
    C.extend(B[B_i:])
    return C

f = OP.OP('rosalind_mer.txt')
input = f.i()

n = input.readline().split()
A = list(map(int, input.readline().split()))
m = input.readline().split()
B = list(map(int, input.readline().split()))

ans = ' '.join(map(str, merge(A, B)))
f.o(ans)
