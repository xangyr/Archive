import queue



def CC(n, A):
    counter = 0
    counter = 0
    graph = {}



    for [i, j] in A:
        if int(i) not in graph:
            graph[int(i)] = []
        if int(j) not in graph:
            graph[int(j)] = []
        graph[int(j)] += [int(i)]
        graph[int(i)] += [int(j)]
    print(graph)
    visited = [int(1)]
    Q = queue.Queue(n)
    Q.put(int(1))
    ccs = [[i+1] for i in range(n)]
    for i in range(n):
        if i+1 not in visited:
            Q.put(int(i+1))
            visited.append(int(i+1))
            while Q.qsize() != 0:
                current = Q.get()
                if current not in graph:
                    visited.append(int(i+1))
                    break
                for i in graph[current]:
                    if i not in visited:
                        Q.put(i)
                        visited.append(i)

            counter += 1



    return counter




with open('rosalind_cc.txt') as input:
    n, m = map(int, input.readline().strip().split())

    A = [list(map(int, i.split())) for i in input]


output = CC(n,A)
print(output)
