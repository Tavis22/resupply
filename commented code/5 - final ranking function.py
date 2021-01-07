"the following functions are taken from '3-ranking partitions' and '4-ranking permutations'"
def getPermCode(permutation):
    depth = len(permutation)
    ordered = sorted(permutation)
    code = []
    for i in permutation:
        edge = ordered.index(i)
        code.append(edge)
        del(ordered[edge])
    return code

from math import factorial

def getPermIndex(permutation):
    code = getPermCode(permutation)
    maxDepth = len(code)
    order = 0
    while len(code) > 0:
        order += factorial(maxDepth - len(code))*code.pop(-1)
    return order

def getIndexCombinedPerm(comPerm):
    if len(comPerm) == 1: return getPermIndex(comPerm[0])
    baseindex = getPermIndex(comPerm[0])
    for perm in comPerm[1:]:
        baseindex *= factorial(len(perm))
    return baseindex + getIndexCombinedPerm(comPerm[1:])

def getSize(partition):
    size = 0
    for group in partition:
        size += len(group)
    return size

def getPartitionCode(partition):
    size = getSize(partition)
    groups = len(partition)
    code = []
    for element in range(2, size + 1):
        for group in range(groups):
            if element in partition[group]:
                code.append(group)
    return code

"______________________________________________________________________________________________________________________________________"


"this function counts the number of total possible combined permutations at a given endpoint (i.e. the number of valid solutions)"
def permutationsAtEndpoint(code):
    count = 1
    newcode = [i for i in code]
    newcode.insert(0,0)
    groupcounts = []
    for i in range(max(newcode)+1):
        groupcounts.append(newcode.count(i))
    for j in groupcounts:
        count *= factorial(j)
    return count


"this is a recursive function which returns the number of permutations total at all endpoints that exist at the desired depth downstream from a vertex"
def downstreamPermCount(code, maxDepth):
    count = 0
    if len(code) == maxDepth: return permutationsAtEndpoint(code)
    branches = max(code) + 2
    for i in range(branches):
        count += downstreamPermCount(code + [i], maxDepth)
    return count

"this function returns the index of any solution. It begins by indexing the combined permutation for the given partition, then adds the number of solutions at each"
"of the lower rank partitions"
def getSolutionIndex(solution):
    partitionCode = getPartitionCode(solution)
    maxPartitionDepth = len(partitionCode)
    index = getIndexCombinedPerm(solution) 
    while len(partitionCode) > 0:
        for i in range(partitionCode[-1]):
            partitionCode[-1] = i
            index += downstreamPermCount(partitionCode, maxPartitionDepth)
        del(partitionCode[-1])
    return index

"____________________________________________________________________________________________________________________"

"The below is for testing purposes, code imported from other sections - results, it works"


##def expandPartitionList(inputPartitionList, newterm):
##    newPartitionList = []
##    for partition in inputPartitionList:
##        for i in range(len(partition)):
##            newpartition = []
##            for j in range(len(partition)):
##                if i == j: newpartition.append(partition[j] + [newterm])
##                else: newpartition.append(partition[j])
##            newPartitionList.append(newpartition)
##        newPartitionList.append(partition + [[newterm]])
##    return newPartitionList
##
##
##def listOfPartitions(numberOfElements):
##    partitionList = [[[1]]]
##    for i in range(2,numberOfElements+1): partitionList = expandPartitionList(partitionList, i)
##    return partitionList
##
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
##def solutionSpace(F): return fullList(listOfPartitions(F))
##
##testSolutions = solutionSpace(6)
##
##for i in range(len(testSolutions)):
##    if i != getSolutionIndex(testSolutions[i]): print(False)



