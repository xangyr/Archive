

import operator
def majority_element(A,m):
    elements = {}

    for i in range(m):
        j = A[i]

        if j in elements:
            elements[j] += 1


        elif j not in elements:
            elements[j] = 1
    elements = sorted(elements.items(), key=operator.itemgetter(1))


    return elements[len(elements)-1][0] if elements[len(elements)-1][1] > m/2 else -1



with open('rosalind_maj.txt') as input:
    n, m = map(int, input.readline().strip().split())

    A = [i.split() for i in input]




output = [str(majority_element(i, m)) for i in A]
print(output)
output = " ".join(output)
text_file = open("sample.txt", "w")
text_file.write(output + " ")

text_file.close()