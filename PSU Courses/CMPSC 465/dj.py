import queue
from queue import PriorityQueue


def BFS(n, A):
    d = n * [0]
    for i in range(1,n):
        d[i] = -1

    graph = {}

    for [i, j] in A:
        if int(i) not in graph:
            graph[int(i)] = []
        graph[int(i)] += [int(j)]

    visited = []
    Q = PriorityQueue(n)
    Q.put(int(1))
    while Q.qsize() != 0:
        current = Q.get()

        if current not in graph.keys():
            continue
        for i in graph[current]:
            if i not in visited:
                Q.put(i)
                visited.append(i)
                d[int(i)-1] = d[int(current) - 1] + 1
    print(d)
    return d





with open('rosalind_bfs (1).txt') as input:
    n, m = map(int, input.readline().strip().split())

    A = [list(map(int, i.split())) for i in input]


output = [str(i) for i in BFS(n,A)]
print(output)
output = " ".join(output)

text_file = open("sample.txt", "w")
text_file.write(output + " ")

text_file.close()