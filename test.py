import nonogram
nng = nonogram.Nonogram(5,5)
nng.addline(0, [2], [0])
nng.addline(0, [1,1,1], [0,0,0])
nng.addline(0, [2,2], [0,0])
nng.addline(0, [3], [0])
nng.addline(0, [1], [0])

nng.addline(1, [3], [0])
nng.addline(1, [1,1], [0,0])
nng.addline(1, [1,1], [0,0])
nng.addline(1, [3], [0])
nng.addline(1, [3], [0])