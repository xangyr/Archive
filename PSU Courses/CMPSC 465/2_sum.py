import string
import OP

def two_sum(A, m):
    for i in range(m):
        if -A[i] in A[i+1:]:
            for j in range(i+1,m):
                if A[i] == -A[j]:
                    return ' '.join([str(i + 1), str(j + 1)])
    return '-1'

f = OP.OP('rosalind_2sum.txt')
input = f.i()
k, m = map(int, input.readline().split())
#A = input.readlines()
ans = []
for i in range(k):
    A = list(map(int, input.readline().split()))
    ans.append(two_sum(A, m))
ans = '\n'.join(ans)
f.o(ans)