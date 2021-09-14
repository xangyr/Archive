import copy

#Reference https://en.wikipedia.org/wiki/3SUM
def three_sum(A, m):
    a, b, c = 0, 0, 0
    C = copy.deepcopy(A)
    A = sorted(A)
    output = []
    for i in range(m - 2):
        lower = i + 1
        upper = m- 1
        while lower < upper:
            a, b, c = A[i], A[lower], A[upper]
            if a + b + c > 0:
                upper -= 1
            elif a + b + c < 0:
                lower += 1
            elif a + b + c == 0:
                output = [C.index(a) + 1] + [C.index(b)+1] + [C.index(c)+1]
                output.sort()
                return [str(i) for i in output]

    return [str(-1)]




with open('rosalind_3sum (3).txt') as input:
    n, m = map(int, input.readline().strip().split())

    A = [list(map(int, i.split())) for i in input]




output = [three_sum(i,m) for i in A]
print(output)

text_file = open("sample.txt", "w")
for i in output:
    t = " ".join(i) + "\n"
    text_file.write(t)