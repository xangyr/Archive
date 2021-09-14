# reference https://en.wikipedia.org/wiki/Binary_search_algorithm
import string

def bs(l, k):
    l_i = 0
    r_i = len(l) - 1
    while l_i <= r_i:
        mid = int(round((l_i + r_i) / 2))
        if l[mid] > k:
            r_i = mid - 1
        elif l[mid] == k:
            return mid + 1
        else:
            l_i = mid + 1
    return -1

input = open('rosalind_bins.txt')
n = int(input.readline().strip())
m = int(input.readline().strip())
A = list(map(int, input.readline().split()))
key = list(map(int, input.readline().split()))
input.close()

output = ' '.join([str(bs(A, k)) for k in key])
f = open('bs_ans.txt', 'w')
f.write(output + ' ')
f.close()