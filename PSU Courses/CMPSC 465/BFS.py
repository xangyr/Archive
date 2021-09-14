from OP import OP
import queue

def BFS(A, n):
    d = [-1 for i in range(n)]
    d[0] = 0
    g = {}
    for a in A:
        if a[0] not in g:
            g[a[0]] = []
    visited = []
    Q = queue.Queue(n)
    while len(Q) != 0:
        z = Q.pop(0)
        for n in range(size):
            if D[n] == -1 and graph[z][n] == 1:
                Q.append(n)
            if a not in visited:
                Q.put(a)
                visited.append(a)
    return d
