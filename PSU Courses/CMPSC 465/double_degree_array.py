def double_degree_array(n, A):
    d = n * [0]
    adj = n * [""]
    d_d = n * [0]

    for [i, j] in A:
        d[int(i) - 1] += 1
        d[int(j) - 1] += 1
        adj[int(i) -1] += "{} ".format(j)
        adj[int(j) -1] += "{} ".format(i)
    for i in range(n):
        t = adj[i].split()
        for j in t:
            if t != None:
                d_d[i] += d[int(j) - 1]
                
    return d_d

