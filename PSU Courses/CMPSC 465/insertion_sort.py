import string

def ins(A, n):
    counter = 0
    for k in range(1, len(A)):
        while k > 0 and A[k] < A[k-1]:
            A[k-1], A[k] = A[k], A[k-1]
            k -= 1
            counter += 1
    return counter

input = open('rosalind_ins.txt')
n = int(input.readline().split()[0])
A = list(map(int, input.readline().split()))
input.close()

print(ins(A, n))