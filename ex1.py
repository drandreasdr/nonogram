import nonogram
nng = nonogram.Nonogram(5, 5)
nng.addline(0, [2], [1])
nng.addline(0, [1,1,1], [1,1,1])
nng.addline(0, [2,2], [1,1])
nng.addline(0, [3], [1])
nng.addline(0, [1], [1])

nng.addline(1, [3], [1])
nng.addline(1, [1,1], [1,1])
nng.addline(1, [1,1], [1,1])
nng.addline(1, [3], [1])
nng.addline(1, [3], [1])

nng.solve()