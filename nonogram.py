##TODO:
##>Might save computational time if I do the following after finding the first solution: check validity across whole board, not just masterline 0 up to current.
##^NO! SHOULDN'T LOOK AT ANYTHING BELOW!

import copy
import line
import numpy as np

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
    def __init__(self, nrows, ncols):
        """
        Just initializes row and col lists. Other methods take care of setting them up.
        """
        self.nrowscols = (nrows, ncols)
        self.rowscols = [[],[]]
        self.masterdim = 0 #change setting to alter along which dimension recursive solution is performed
        self.slavedim = 1 - self.masterdim
        self.nmasterslave = [self.nrowscols[i] for i in [self.masterdim, self.slavedim]]
        self.issetupcomplete = False
        self.validsolutionjustfound = False

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
        assert len(self.rowscols[dim]) <= self.nrowscols[dim], "No more lines can be added for this dimension"
        linelength = self.nrowscols[1-dim] #length of line is length of the other dimension
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
            if len(self.rowscols[i]) != self.nrowscols[i]:
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
                    if i_masterline == self.nmasterslave[0]-1: #at last line
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
            uncoveredconf = [-1]*(self.nrowscols[self.masterdim])
            uncoveredconf[:curmasteridx+1] = partialcol
            if not self.rowscols[self.slavedim][i].isuncoveredconfvalid(uncoveredconf):
                return False
        return True

    def getboard(self, endidx = None):
        """
        Note that it is the master lines that store the configuration of the board
        """
        if endidx == None:
            endidx = self.nmasterslave[0]
        #The board (possibly partial):
        board = np.array([self.rowscols[self.masterdim][i].getconfiguration() for i in range(endidx)])
        if self.masterdim == 1:
            board = board.T
        return board.tolist()