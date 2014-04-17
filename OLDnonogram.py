import copy

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
        self.issetupcomplete = False

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
        assert len(self.rowscols[dim]) <= self.nrowscols[dim], "No more lines can be added for this dimension"
        self.rowscols[dim].append(self.Line(self.nrowscols[dim], seg_length, seg_coloridx))

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

    def hassolution_operative(self):
        """
        Returns true if given
        """
        #Find
        soldim = 0 #0 is default
        hasnextvalidconfiguration_recursive_operative(0, soldim)
        #Do it again to see if there are more than one solution


    def hasnextvalidconfiguration_recursive_operative(self, i_line):
        """
        Returns true if the line sollines[i_line] can be advanced (via setnextcombination()) to
        a configuration that is valid, and for which the next line (if it exists)
        returns True when this same method is called upon it (thereby "recursive").
        "operative": operates on sollines and sollinesperp (administered by
        hassolution_operative(), see description there). Note that if a solution is found,
        self.rowscols[soldim] will contain the corresponding configuration (note that there
        might be multiple valid solutions).
        Note: should only be called by hassolution_operative and by itself
        """
        perpdim = 1 - soldim
        while True:
            if self.rowscols[soldim][i_line].hasmorecombinations():
                self.rowscols[soldim][i_line].setnextcombination()
                if isboardvalid():
                    if i_line == n_line-1: #at last line
                        return True
                    if hasvalidcombination_recursive_operative(i_line+1): #recursive call
                        return True
                    #TODO try to combine the above two as soon as everything works, make sure it short circuits
            else: #if no more combinations
                return False


    class Line:
        """
        Represents a row or a column in the nonogram. It stores a list of Segments.
        The Lines of the Nonogram are used to store the rules defining it. It can
        also optionally be used to store the configuration of the nonogram (a
        functionality which is used by the solver), although this configuration
        is separate from the one stored in "configuration" (which is mostly used in relation
        to the "player" interface).
        Stores:
        length: number of blocks in the Line
        segments: a list of Segments.
        uncoveredblocks: a list of uncovered blocks
        """
        def __init__(self, length, seg_length, seg_coloridx):
            self.length = length
            self.segments = []
            for i in range(len(seg_length)):
                self.appendsegment(seg_length[i], seg_coloridx[i])
            self.setinitialconfiguration()

        def appendsegment(self, length, coloridx):
            """
            Appends a new Segment to the Line, if there is room for it. Adds an
            "emptytail" to the previous Segment if needed.
            """
            #No plans to add a method "removesegment()" yet.
            #Can't define position of segmednt here: this method is for setting
            #up the Nonogram, that functionality would belong to manipulating/solving the Nonogram
            insertemptytail = False
            templength = length
            if len(self.segments) > 0 and coloridx == self.segments[-1].coloridx:
                #previous segment exists and has the same color
                insertemptytail = True
                templength += 1
            if self.gettotallengthofsegments() + templength > self.length:
                #total length of all segments is too long if current segment is added
                raise ArgumentError("Total segment length exceeds Line length if current segment is added")
            #If here, go ahead and add Segment after perhaps adding an emptytail to previous segment:
            if insertemptytail:
                self.segments[-1].emptytail = True
            self.segments.append(self.Segment(length, coloridx))

        def gettotallengthofsegments(self):
            length = 0
            for seg in self.segments:
                length += seg.getfulllength()
            return length


        def setinitialconfiguration(self):
            """
            Positions all segments "as early as possible"
            """
            self.segments[0].pos = 0
            self.movesegmentscloseafter(0)

        def movesegmentscloseafter(self, i):
            pos = self.segments[i].pos
            for i_seg in range(i, len(self.segments)): #loop over subsequent segments
                seg = self.segments[i_seg]
                seg.pos = pos
                pos += seg.getfulllength()
            assert pos <= self.length

        def getconfiguration(self):
            """
            Returns a list of color indices corresponding to the given
            """
            conf = [0]*self.length
            for seg in self.segments:
                for i in range(0, seg.length):
                    conf[seg.pos+i] = seg.coloridx
            return conf

        def hasnextconfiguration(self):
            """
            Whether the configuation of the given line can be incremented. False if the end position has been reached by all segments.
            """
            pos = self.length
            for seg in reversed(self.segments):
                pos -= seg.getfulllength()
                if seg.pos != pos:
                    return True
            return False

        def setnextconfiguration(self):
            i_seg = len(self.segments) - 1
            if self.issegmentincrementable(i_seg):
                self.segments[i_seg].pos += 1
                return #we're done here
            #If still here, then go backwards until finding an incrementable segment:
            done = False
            while not done:
                i_seg -= 1
                assert i_seg >= 0 #should only be needed if caller forgets to call hasnextconfiguration() first
                if self.issegmentincrementable(i_seg):
                    done = True
            #Now, increment given segment and position all others tightly after it:
            self.segments[i_seg].pos += 1
            self.movesegmentscloseafter(i_seg)

        def issegmentincrementable(self, i_seg):
            """
            Returns True if position of given segment can be incremented.
            """
            posafter = self.segments[i_seg].pos + self.segments[i_seg].getfulllength() #first position after given segment
            if i_seg == len(self.segments) - 1:
                #segment is last segment
                if posafter >= self.length: #segment falls outside of board
                    return False
            else:
                #segment is not last segment
                nextseg = self.segments[i_seg + 1]
                if posafter >= nextseg.pos: #segment overlaps next segment
                    return False
            return True

        class Segment:
            """
            Represents an uninterrupted sequence of blocks and is included in a Line.
            If the following Segment in the Line is of the same color, the segment has an "emptytail":
            A trailing empty block
            Stores:
            length: number of colored blocks in the Segment
            coloridx: the color index of the Segment (mapping to colors defined by Nonogram)
            emptytail:
            pos: its position within its parent Line. -1 means not assigned (initialization value)
            """
            def __init__(self, length, coloridx):
                self.length = length
                self.coloridx = coloridx
                self.emptytail = False
                self.pos = -1

            def getfulllength(self):
                """
                Gets the length of the string including the length (1) of the potential emptytail
                """
                if self.emptytail:
                    return self.length+1
                else:
                    return self.length


##TODO: Write some tests for adding segments etc. See the algorithms-github repo for format for tests