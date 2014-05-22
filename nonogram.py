##TODO:
##>Might save computational time if I do the following after finding the first solution: check validity across whole board, not just masterline 0 up to current.
##^NO! SHOULDN'T LOOK AT ANYTHING BELOW!
import copy
import line
import numpy as np
#For NonogramVisualizer only:
import grid.grid as grid
import pygame

class NonogramVisualizer:

    """
    Stores and plots a Nonogram object
    topleftpos and dimensions (float tuples) determine its size and position
    """
    def __init__(self, nonogram, topleftpos, dimensions):
        self.nonogram = nonogram
        self.topleftpos = topleftpos
        self.dimensions = dimensions
        #Set up positions of draw areas:
        maxnseg = tuple(max([len(rowcol.segments) for rowcol in nonogram.rowscols[i]]) for i in range(2))
        cellsize = min(self.dimensions[i]/(maxnseg[i] + nonogram.nrowcol[1-i]) for i in range(2))
        rowboxwidth = maxnseg[0]*cellsize
        colboxheight = maxnseg[1]*cellsize
        mainboardtopleftpos = (topleftpos[0] + rowboxwidth, topleftpos[0] + colboxheight)
        mainboarddims = tuple(cellsize*nonogram.nrowcol[i-1] for i in range(2))
        #rowboxdims = (rowboxwidth, mainboarddims[1])
        #colboxdims = (mainboarddims[0], colboxheight)

        self.mainboard = self.MainBoard(nonogram, mainboardtopleftpos, cellsize, nonogram.nrowcol)
        self.rowbox = self.LineBox(nonogram, 0, (topleftpos[0], mainboardtopleftpos[1]), rowboxwidth, cellsize)
        self.colbox = self.LineBox(nonogram, 1, (mainboardtopleftpos[0], topleftpos[1]), colboxheight, cellsize)

    def draw(self, displaysurf):
        #Draw main board:
        self.mainboard.draw(displaysurf)
        #Draw line boxes:
        self.rowbox.draw(displaysurf)
        self.colbox.draw(displaysurf)


    class LineBox:
        def __init__(self, nonogram, dim, topleftpos, depth, cellsize):
            self.nonogram = nonogram
            self.dim = dim
            self.topleftpos = topleftpos
            self.depth = depth
            self.cellsize = cellsize

            #Font to be used
            self.font = pygame.font.Font(None, int(cellsize))
            self.fontcolor = (255, 255, 255)
            self.fontcolor_alternative = (0, 0, 0) #used if cell color is close enough to fontcolor
            #Create list of grids:
            self.linegrids = [None]*nonogram.nrowcol[dim]
            for i_line, line in enumerate(nonogram.rowscols[dim]):
                segs = line.segments
                #Top left position and nrowcol:
                topleftpos_linegrid = [0]*2
                topleftpos_linegrid[dim] = topleftpos[dim] + depth - len(segs)*cellsize
                topleftpos_linegrid[1-dim] = topleftpos[1-dim] + i_line*cellsize
                nrowcol_linegrid = [0]*2
                nrowcol_linegrid[dim] = 1
                nrowcol_linegrid[1-dim] = len(segs)
                #Colors:
                colors_linegrid = [0]*len(segs)
                for i_seg, seg in enumerate(segs):
                    colors_linegrid[i_seg] = nonogram.colormap[seg.coloridx]
                #Create grid:
                linegrid = grid.Grid(topleftpos_linegrid, (cellsize, cellsize), nrowcol_linegrid, borderwidth = 1, colors = colors_linegrid)
                self.linegrids[i_line] = linegrid

        def draw(self, displaysurf):
            for i_line, linegrid in enumerate(self.linegrids):
                linegrid.draw(displaysurf)
                #Draw text:
                textpos = list(linegrid.xy)
                for i_seg in range(linegrid.nrowcol[1-self.dim]):
                    number = self.nonogram.rowscols[self.dim][i_line].segments[i_seg].length
                    fontsurf = self.font.render(str(number), True, self.fontcolor)
                    displaysurf.blit(fontsurf, textpos)
                    textpos[self.dim] += self.cellsize

    class MainBoard:
        def __init__(self, nonogram, topleftpos, cellsize, nrowcol):
            self.nonogram = nonogram
            self.topleftpos = topleftpos
            self.cellsize = cellsize
            self.nrowcol = nrowcol

            self.grid = grid.Grid(topleftpos, (cellsize, cellsize), nrowcol, 5, 2)
            board = self.nonogram.firstsolvedboard
            for i in range(nonogram.nrowcol[0]):
                for j in range(nonogram.nrowcol[1]):
                    color = nonogram.colormap[board[i][j]]
                    self.grid.setcolor(i, j, color)


        def draw(self, displaysurf):
            self.grid.draw(displaysurf)

class Nonogram:
    """
    Stores:
    rowscols: a list containing two lists of Line objects, representing rows and cols, respectively.
    Contains rules and can also describe the configuration of the Nonogram.
    configuration: 2D list containing color indices, representing the (partial or
    complete) configuration of the Nonogram. Separate from the configuration (used by the solver) as described by
    the state of the Line objects.
    colormap: list of hexadecimal color codes. 0:th element empty ?TODO?
    Note: cells are identified by a number: -1: unknown, 0: known and empty,
    > 0: colors as described by "colormap"
    """
    def __init__(self, nrow, ncol, colormap):
        """
        Just initializes row and col lists. Other methods take care of setting them up.
        """
        self.nrowcol = (nrow, ncol)
        self.rowscols = [[],[]]
        self.masterdim = 0 #change setting to alter along which dimension recursive solution is performed
        self.slavedim = 1 - self.masterdim
        #self.nmasterslave = [self.nrowcol[i] for i in [self.masterdim, self.slavedim]]
        self.issetupcomplete = False
        self.validsolutionjustfound = False
        self.colormap = ((255,255,255),) + colormap

    def setup(self):
        #Open text file, read color indices and set up, find ROWS line, define rows, find COLS line, define cols.
        pass

    def setcolorindices(self, colors):
        """
        colors: a list of hexadecimal color codes
        """
        self.colormap = colors
        pass

    def addline(self, dim, seg_length, seg_coloridx):
        """
        Adds a Line consisting of segments of quantity and color defined by the input parameters
        dim: dimension: 0 for row, 1 for col
        seg_length: list of quantities of added segments
        seg_color: list of color indices of added segments
        Note: the method Segment.appendsegment() will warn if the line is overcrowded.
        """
        assert len(seg_length) == len(seg_coloridx), 'List of segment lengths and list of segment color indices not equal in length'
        assert len(self.rowscols[dim]) <= self.nrowcol[dim], "No more lines can be added for this dimension"
        linelength = self.nrowcol[1-dim] #length of line is length of the other dimension
        newline = line.Line(linelength, seg_length, seg_coloridx)
        if dim == self.masterdim:
            newline.setinitialconfiguration()
        self.rowscols[dim].append(newline)
        self.setissetupcomplete()

    def setissetupcomplete(self):
        """
        Checks if setup of nonogram is complete (i.e. all rows and cols have been defined)
        """
        issetupcomplete = True
        for i in range(len(self.rowscols)):
            if len(self.rowscols[i]) != self.nrowcol[i]:
                issetupcomplete = False
        self.issetupcomplete = issetupcomplete

    def solve(self):
        """
        """
        hasnextsolution = self.setnextvalidconfiguration(0)
        if hasnextsolution == True:
            self.firstsolvedboard = self.getboard()
            self.validsolutionjustfound = True
            print("Solution found (and stored)")
            #Check if there are multiple solutions:
            hasnextsolution = self.setnextvalidconfiguration(0)
            if hasnextsolution == True:
                self.secondsolvedboard = self.getboard()
                print("Solution not unique, second solution stored")
            else:
                print("...and solution is unique!")
        else:
            print("No solution")



    def setnextvalidconfiguration(self, i_masterline):
        """
        Attempts (and returns True if possible) to advance the line sollines[i_masterline]
        (via setnextcombination()) to a configuration that is valid, and for which
        the next line (if it exists) returns True when this same method is called
        upon it (thereby "recursive"). Note that
        if a solution is found, self.rowscols[self.masterdim] will then contain the corresponding
        configuration (note that there might be multiple valid solutions).
        Note: should only be called by hassolution_operative and by itself
        """
        curmasterline = self.rowscols[self.masterdim][i_masterline]
        #Always start testing from the initial configuration:
        if not self.validsolutionjustfound:
            curmasterline.setinitialconfiguration()
        while True:
            if self.validsolutionjustfound:
                self.validsolutionjustfound = False
                #and skip directly to setting next conf (if possible)
            else:
                if self.isboardvalid(i_masterline): #
                    if i_masterline == self.nrowcol[self.masterdim] - 1: #at last line
                        return True
                    if self.setnextvalidconfiguration(i_masterline+1): #recursive call
                        return True
                    #TODO try to combine the above two as soon as everything works, make sure it short circuits
            if curmasterline.hasnextconfiguration():
                curmasterline.setnextconfiguration()
            else: #if no more combinations
                return False

    def isboardvalid(self, curmasteridx):
        """
        Returns True if the board - as far as currently revealed - is in agreement with
        the segment configuration of the slave lines. Assumes that it is in agreement
        with the master lines and that the revealed portion of the board corresponds
        to the first N master lines, N between 0 and the number of lines.
        """
        #Create uncoveredconf
        masterlines = self.rowscols[self.masterdim]
        uncoveredboard = [masterlines[i].getconfiguration() for i in range(curmasteridx+1)]
        partialcols = tuple(zip(*uncoveredboard)) #maybe use numpy instead?
        for i, partialcol in enumerate(partialcols):
            uncoveredconf = [-1]*(self.nrowcol[self.masterdim])
            uncoveredconf[:curmasteridx+1] = partialcol
            if not self.rowscols[self.slavedim][i].isuncoveredconfvalid(uncoveredconf):
                return False
        return True

    def getboard(self, endidx = None):
        """
        Note that it is the master lines that store the configuration of the board
        """
        if endidx == None:
            endidx = self.nrowcol[self.masterdim]
        #The board (possibly partial):
        board = np.array([self.rowscols[self.masterdim][i].getconfiguration() for i in range(endidx)])
        if self.masterdim == 1:
            board = board.T
        return board.tolist()

def readnonogramfromfile(filename):
    def inputlinetononogramline(inputline):
        lineparts = inputline.replace(" ", "").split(";")
        #Segment lengths:
        seg_length = list(map(int, lineparts[0].split(",")))
        #Colors:
        if len(lineparts) == 1:
            seg_coloridx = [1]*len(seg_length)
        else:
            seg_coloridx = list(map(int, lineparts[1].split(",")))
        return (seg_length, seg_coloridx)

    with open('input/' + filename, 'r') as f:
        section = 0
        headers = ["COLORS", "ROWS", "COLS"]
        colors = []
        rows = [[],[]]
        cols = [[],[]]
        for rawinputline in f:
            inputline = rawinputline.rstrip("\n")
            if inputline in headers: #arrived at a header
                section += 1
                continue
            if len(inputline) == 0 or not inputline[0].isnumeric():
                continue

            if section == 1:
                color_str = inputline.replace(" ", "").split(",")
                color = tuple(map(int, color_str))
                colors.append(color)
            elif section == 2:
                linedata = inputlinetononogramline(inputline)
                rows[0].append(linedata[0])
                rows[1].append(linedata[1])
            elif section == 3:
                linedata = inputlinetononogramline(inputline)
                cols[0].append(linedata[0])
                cols[1].append(linedata[1])

        assert section == 3, "Not complete"

        #Construct nonogram:
        colors = tuple(colors)
        nrows = len(rows[0])
        ncols = len(cols[0])
        nonogram = Nonogram(nrows, ncols, colors)
        for i in range(nrows):
            nonogram.addline(0, rows[0][i], rows[1][i])
        for i in range(ncols):
            nonogram.addline(1, cols[0][i], cols[1][i])
        return nonogram
