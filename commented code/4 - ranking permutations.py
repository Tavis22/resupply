"this function generates a code for a particular permutation - the code is a list of the branches taken to arrive at that node"
def getCode(permutation):
    depth = len(permutation)
    ordered = sorted(permutation)
    code = []
    for i in permutation:
        edge = ordered.index(i)
        code.append(edge)
        del(ordered[edge])
    return code

from math import factorial

"This function returns the index for a particular permutation"
"the behaviour of the tree is very regular, the number of endpoints for given node is the factorial of difference in depth form the node to the maxdepth"
def getIndex(permutation):
    code = getCode(permutation)
    maxDepth = len(code)
    index = 0
    while len(code) > 0:
        index += factorial(maxDepth - len(code))*code.pop(-1)
    return index

"Now we must rank the combined permutations, eg: [[5, 1], [2, 4, 3]]"
def getIndexCombined(comPerm):
    if len(comPerm) == 1: return getIndex(comPerm[0])
    baseindex = getIndex(comPerm[0])
    for perm in comPerm[1:]:
        baseindex *= factorial(len(perm))
    return baseindex + getIndexCombined(comPerm[1:])

"taking earlier code to produce a list of combined permutations to test the indexing function - result: it works"

##from itertools import permutations, product 
##
##def fullList(partitionList):
##    fullList = []
##    for partition in partitionList:
##        permutationListNested = []
##        for set in partition:
##            permutationListNested.append(list(permutations(set)))
##        fullList += list(product(*permutationListNested))
##    return fullList
##
##testpartition = [[[1],[2,4,8,12],[7,9,10],[3,6,11],[13]]]
##
##testlist = fullList(testpartition)
##
##for i in range(len(testlist)):
##    print(i == getIndexCombined(testlist[i]))