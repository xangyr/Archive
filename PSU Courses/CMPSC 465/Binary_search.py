import string

def binary_search(A, i):
    L = 0
    R = len(A) - 1
    while L <= R:
        mid = int(round((L + R) / 2))
        if A[mid] == i:
            return mid + 1

        if A[mid] > i:
            R = mid - 1
        else:
            L = mid + 1
    return -1


with open('rosalind_bins.txt') as input:
    n, m = [int(input.readline().strip()) for repeat in range(2)]

    A = list(map(int, input.readline().strip().split()))

    d = list(map(int, input.readline().strip().split()))


output = [str(binary_search(A, i)) for i in d]



output = " ".join(output)
text_file = open("sample01.txt", "w")
text_file.write(output + " ")
text_file.close()

#reference https://en.wikipedia.org/wiki/Binary_search_algorithm