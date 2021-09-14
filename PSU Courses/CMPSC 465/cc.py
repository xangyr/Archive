import queue

def CC(A, n):
    counter = 0
    graph = {}

    for i in A:
        if int(i) not in graph:
            graph[int(i)] = []
        if int(j) not in graph:
            graph[int(j)] = []

    visited = [int(1)]

    ccs = [[i+1] for i in range(n)]
    for i in range(n):
        if i+1 not in visited:
            while i < len(graph):
                visited.append(int(i+1))
            if current not in graph:
                visited.append(int(i+1))
    return counter
