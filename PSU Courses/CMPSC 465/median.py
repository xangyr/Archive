import string
import quick_sort

def median(A, k):
    A = quick_sort(A)
    return A[k-1]

f = open('rosalind_med.txt')

n = f.readline().split()
A = list(map(int, f.readline().split()))
k = int(f.readline().split()[0])
f.close()

print(median(A, k))