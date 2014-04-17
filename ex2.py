import nonogram
nng = nonogram.Nonogram(5,5)
#seg_length, #seg_coloridx
nng.addline(0, [3], [1])
nng.addline(0, [5], [1])
nng.addline(0, [5], [1])
nng.addline(0, [1,1,1], [1,2,1])
nng.addline(0, [1], [2])

nng.addline(1, [2], [1])
nng.addline(1, [4], [1])
nng.addline(1, [3,2], [1,2])
nng.addline(1, [4], [1])
nng.addline(1, [2], [1])

nng.solve()