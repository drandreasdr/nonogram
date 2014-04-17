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
            self.segments[-1].addemptytail()
        self.segments.append(self.Segment(length, coloridx))

    def gettotallengthofsegments(self):
        length = 0
        for seg in self.segments:
            length += seg.lengthfull
        return length

    def getconfiguration(self):
        """
        Returns a list of color indices corresponding to the given
        """
        conf = [0]*self.length
        for seg in self.segments:
            assert seg.pos >= 0, 'At least one segment not initialized'
            for i in range(0, seg.length):
                conf[seg.pos+i] = seg.coloridx
        return conf

    class Segment:
        """
        Represents an uninterrupted sequence of blocks and is included in a Line.
        If the following Segment in the Line is of the same color, the segment has an "emptytail":
        A trailing empty block
        Stores:
        length: number of colored blocks in the Segment
        coloridx: the color index of the Segment (mapping to colors defined by Nonogram)
        _emptytail: private: it shouldn't be manipulated directly, because lengthfull must be
        modified whenever this variable is.
        pos: its position within its parent Line. -1 means not assigned (initialization value)
        """
        def __init__(self, length, coloridx):
            self.length = length
            self.coloridx = coloridx
            #Defaults:
            self._emptytail = False
            self.lengthfull = length
            self.pos = -1

        def addemptytail(self):
            self._emptytail = True
            self.lengthfull = self.length + 1

        def hasemptytail(self):
            return self._emptytail

        def getcoloridxatpos(self, pos):
            assert pos >= 0 and pos < self.lengthfull
            if pos == self.lengthfull - 1 and self.hasemptytail():
                return 0
            else:
                return self.coloridx

        def getposaftersegment(self):
            assert self.pos >= 0
            return self.pos + self.lengthfull

        def matches(self, conf):
            """
            Checks whether given segment matches the pattern conf (must be equal
            to the segment in *length)
            """
            assert len(conf) == self.lengthfull
            for i in range(self.length):
                if conf[i] != self.getcoloridxatpos(i):
                    return False
            return True

        def matchespotentially(self, conf):
            """
            Checks whether given segment matches the pattern conf (must be equal
            to the segment in length) potentially, i.e. unknown blocks are ok.
            """
            assert len(conf) == self.lengthfull
            for i in range(self.lengthfull):
                if conf[i] >= 0 and conf[i] != self.getcoloridxatpos(i):
                    return False
            return True

class MasterLine(Line):
    """
    The Line subclass that is recursively iterated upon in order to find the Nonogram solution.
    """
    def __init__(self, length, seg_length, seg_coloridx):
        super().__init__(length, seg_length, seg_coloridx)
        self.setinitialconfiguration()

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
            pos += seg.lengthfull
        assert pos <= self.length

    def hasnextconfiguration(self):
        """
        Whether the configuation of the given line can be incremented. False if the end position has been reached by all segments.
        """
        pos = self.length
        for seg in reversed(self.segments):
            pos -= seg.lengthfull
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
        posafter = self.segments[i_seg].getposaftersegment() #first position after given segment
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

class SlaveLine(Line):
    """
    The Line subclass that is used for lines perpendicular to the MasterLine objects.
    """

    def __init__(self, length, seg_length, seg_coloridx, uncoveredconf):
        super().__init__(length, seg_length, seg_coloridx)
        self.uncoveredconf = uncoveredconf

    def isuncoveredconfvalid(self):
        pos = 0
        for seg in self.segments:
            done = False
            while not done:
                if pos + seg.lengthfull >= self.length: #using getposaftersegment doesn't work since segments aren't actually moved
                    return False
                if seg.matchespotentially(self.uncoveredconf[pos:pos+seg.lengthfull]):
                    pos += seg.lengthfull #skip over current segment...
                    done = True #...and go to next segment
                else:
                    if self.uncoveredconf[pos] > 0: #non-empty block passed
                        return False
                    pos += 1
        #if still here, uncoveredconf is valid
        return True