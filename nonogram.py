class Nonogram:
    """
    Stores:
    rows, cols: both lists of Line objects
    colormap: list of hexadecimal color codes. 0:th element empty ?TODO?
    """
    def __init__(self, ):
        1

    def hasvalidcombination_recursive_operative(self, i_line):
        """
        Returns true if given line has a combination that is valid, and for which the next line (if it exists) returns True when this same method is called upon it
        Note: Should only be called by hassolution_operative and by itself
        """
        moremovesavailable = False
        while moremovesavailable:
            if nonogramsolvee.line[i_line].hasmorecombinations():
                nonogramsolvee.line[i_line].setnextcombination()
                if isboardvalid():
                    if i_line == n_line-1: #at last line
                        return True
                    if hasvalidcombination_recursive_operative(i_line+1): #recursive call
                        return True
                    #TODO try to combine the above two as soon as everything works, make sure it short cicuits
            else: #if no more combinations
                moremovesavailable = False
        #if still here, we have failed to find a valid combination
        return False

    def hassolution_operative(self):
        hasvalidcombination_recursive_operative(self, 0)

    class Line:
        """Represents a row or a column in the nonogram. It stores a
        list of Segments
        Stores:
        nblocks: number of blocks in the Line
        segments: a list of Segments.
        """
        def __init__(self, nblocks, ):
            self.nblocks = nblocks
            self.segments = []
            self.clearpositions()

        def clearpositions(self):
            for seg in segments:
                self.seg_positions[i] = -1;

        def appendsegment(self, nblocks, coloridx):
            """
            Appends a new Segment to the Line, if there is room for it. Adds an
            "emptytail" to the previous Segment if needed.
            """
            #No plans to add a method "removesegment()" yet.
            #Can't define position of segment here: this method is for setting
            #up the Nonogram, that functionality would belong to manipulating/solving the Nonogram
            insertemptytail = False
            templength = nblocks
            if len(self.segments) > 0 and coloridx == self.segments[-1].coloridx:
                #previous segment exists and has the same color
                insertemptytail = True
                templength += 1
            if self.gettotalsegmentlength() + templength > self.nblocks:
                #total length of all segments is too long if current segment is added
                raise ArgumentError("Total segment length exceeds Line length if current segment is added")
            #If here, go ahead and add Segment after perhaps adding an emptytail to previous segment:
            if insertemptytail:
                self.segments[-1].emptytail = True
            self.segments.append(self.Segment(nblocks, coloridx))

        def gettotalsegmentlength(self):
            length = 0
            for seg in segments:
                length += seg.getfulllength()
            return length

        class Segment:
            """
            Represents an uninterrupted sequence of blocks and is included in a Line.
            If the following Segment in the Line is of the same color, the segment has an "emptytail":
            A trailing empty block
            Stores:
            _nblocks: number of colored blocks in the Segment
            coloridx: the color index of the Segment (mapping to colors defined by Nonogram)
            emptytail:
            pos: its position within its parent Line. -1 means not assigned (initialization value)
            """
            def __init__(self, nblocks, coloridx):
                self._nblocks = nblocks
                self.coloridx = coloridx
                self.emptytail = False
                self.pos = -1

            def getfulllength():
                """
                Gets the length of the string including the length (=!) of the potential emptytail
                """
                if emptytail:
                    return self._nblocks+1
                else:
                    return self._nblocks


##TODO: Write some tests for adding segments etc. See the algorithms-github repo for format for tests