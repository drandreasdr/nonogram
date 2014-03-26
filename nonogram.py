#Nonogram class
class NonoGram:
    #
#Returns true if given line has a combination that is valid, and for which the next line (if it exists) returns True when this same method is called upon it
#Note: Should only be called by hassolution_operative and by itself
def hasvalidcombination_recursive_operative(self, i_line):
    moremovesavailable = False
    while moremovesavailable:
        if line[i_line].hasmorecombinations():
            line[i_line].setnextcombination()
            if isboardvalid():
                if i_line == n_line-1: #at last line
                    return True
                if hasvalidcombination_recursive_operative(i_line+1): #recursive call
                    return True
                #TODO try to combine the above two as soon as everything works, make sure it short cicuits
        else: #if no more combinations
            moremovesavailable = False
    #if still here, we done failed to find a valid combination
    return False

class NonoGramSolver:
