"this function generates the partition code corresponding with a given index and network size. It also returns the index of the comPerm of that partition"
"in other words, it travels outwards on the partition tree, removing from the index the number of solutions bypassed on the way"
"(F here is the number of resuplly nodes or force groups)"
def generatePartitionCodeAndPermIndex(F, index):
    if index > maxIndex(F):
        print("choose a lower index")
        return
    maxDepth = F - 1
    count = downstreamPermCount([0], maxDepth)
    if index > count - 1:
        partitionCode = [1]
        index -= count
    else:
        partitionCode = [0]
    while len(partitionCode) < maxDepth:
        branches = max(partitionCode) + 2
        for i in range(branches):
            count = downstreamPermCount(partitionCode + [i], maxDepth)
            if count > index:
                partitionCode.append(i)
                break
            else:
                index -= count
    return partitionCode, index

"the following functions are copied from another section, they are required for the maxIndex function"
from math import factorial

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

def downstreamPermCount(code, maxDepth):
    count = 0
    if len(code) == maxDepth: return permutationsAtEndpoint(code)
    branches = max(code) + 2
    for i in range(branches):
        count += downstreamPermCount(code + [i], maxDepth)
    return count

"this function returns the max index for a given network size, it's a modification of the general getIndex function."
def maxIndex(F):
    maxPartitionCode = []
    for i in range(1, F):
        maxPartitionCode.append(i)
    maxPartitionDepth = F-1
    index = 0 
    while len(maxPartitionCode) > 0:
        for i in range(maxPartitionCode[-1]):
            maxPartitionCode[-1] = i
            index += downstreamPermCount(maxPartitionCode, maxPartitionDepth)
        del(maxPartitionCode[-1])
    return index

"this function generates a partition for a given partition code"
def generatePartition(partitionCode):
    partition = [[1]]
    for i in range(len(partitionCode)):
        if partitionCode[i] > len(partition) - 1:
            partition.append([i+2])
        else: partition[partitionCode[i]].append(i+2)
    return partition

"this function generates a permutation code for a given set size and index"
def generatePermCodeFromIndex(index, setSize):
    maxDepth = setSize
    permCode = []
    while len(permCode) < maxDepth:
        branches = maxDepth - len(permCode)
        PermsPerBranch = factorial(branches - 1) 
        permCode.append(index//PermsPerBranch)
        index = index%PermsPerBranch
    return permCode

"this function generates a permutation from a given permutation code and ordered set"
def PermFromCode(permCode, set):
    permutation = []
    for i in permCode:
        permutation.append(set.pop(i))
    return permutation

"this function returns a list of the individual indexes for each of the permutations in the partition"
def comIndexFromIndex(index, partition):
    groupSizes = []
    for i in partition:
        groupSizes.append(len(i))
    size = len(groupSizes)
    comIndex = []
    for i in range(size-1):
        product = 1
        for j in range(i+1, size):
            product *= factorial(groupSizes[j])
        comIndex.append(index//product)
        index = index%product
    comIndex.append(index)
    return comIndex

"this function generates a combined permutation from a partition of ordered sets and an index"
def comPermFromIndex(index, partition):
    comPerm = []
    comIndex = comIndexFromIndex(index, partition)
    for i in range(len(comIndex)):
        comPerm.append(PermFromCode(generatePermCodeFromIndex(comIndex[i], len(partition[i])),partition[i]))
    return comPerm

"this function generates a solution from a given index and network size"
def generateSolutionFromIndex(index, F):
    partitionCode, comPermIndex = generatePartitionCodeAndPermIndex(F, index)
    partition = generatePartition(partitionCode)
    return comPermFromIndex(comPermIndex, partition)

print(maxIndex(14))

"testing below"

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
##solutionSpace = solutionSpace(6)
##
##for i in range(len(solutionSpace)):
##    print(solutionSpace[i], generateSolutionFromIndex(i, 6))
