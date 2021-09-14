

#reference:https://medium.com/@ssbothwell/counting-inversions-with-merge-sort-4d9910dc95f0

def counting_inversion(A, B):
    C = []

    i = 0
    j = 0
    counter = 0
    while i < len(A) and j < len(B):

        if A[i] > B[j]:
            C += [B[j]]
            j += 1
            counter = counter + len(A) - i
        else:
            C += [A[i]]
            i += 1

    C += A[i:] + B[j:]
    return C, counter


def merge_sort(A, n):
    if n < 2:
        return A, 0

    mid = round(n/2)

    L, L_counter = merge_sort(A[:mid], len(A[:mid]))
    R, R_counter = merge_sort(A[mid:], len(A[mid:]))
    output, counter = counting_inversion(L, R)
    return output, counter + R_counter + L_counter





with open('rosalind_inv.txt') as input:

    n= list(map(int, input.readline().strip().split()))


    A = list(map(int, input.readline().split()))

    output = merge_sort(A,n[0])[1]
    print(output)
