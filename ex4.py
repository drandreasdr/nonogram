import nonogram
nng = nonogram.Nonogram(10,10)
#seg_length, #seg_coloridx
nng.addline(0, [4], [1])
nng.addline(0, [5], [1])
nng.addline(0, [5], [1])
nng.addline(0, [5], [1])
nng.addline(0, [3], [1])
nng.addline(0, [2,3], [1,1])
nng.addline(0, [1,3,1], [1,1,1])
nng.addline(0, [3,2,2], [1,1,1])
nng.addline(0, [6], [1])
nng.addline(0, [3,2], [1,1])

nng.addline(1, [2], [1])
nng.addline(1, [1,1], [1,1])
nng.addline(1, [1,1,1], [1,1,1])
nng.addline(1, [3,1], [1,1])
nng.addline(1, [3,4], [1,1])
nng.addline(1, [4,3], [1,1])
nng.addline(1, [4,1,1], [1,1,1])
nng.addline(1, [5,1], [1,1])
nng.addline(1, [3,3], [1,1])
nng.addline(1, [7], [1])

nng.solve()

#i_masterline == 0 and self.rowscols[self.masterdim][0].segments[0].pos == 3
#How can the second row have moved?