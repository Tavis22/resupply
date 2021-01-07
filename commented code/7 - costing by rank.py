"the following are the functions for deranking"

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

def generatePartition(partitionCode):
    partition = [[1]]
    for i in range(len(partitionCode)):
        if partitionCode[i] > len(partition) - 1:
            partition.append([i+2])
        else: partition[partitionCode[i]].append(i+2)
    return partition

def generatePermCodeFromIndex(index, setSize):
    maxDepth = setSize
    permCode = []
    while len(permCode) < maxDepth:
        branches = maxDepth - len(permCode)
        PermsPerBranch = factorial(branches - 1) 
        permCode.append(index//PermsPerBranch)
        index = index%PermsPerBranch
    return permCode

def PermFromCode(permCode, set):
    permutation = []
    for i in permCode:
        permutation.append(set.pop(i))
    return permutation

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

def comPermFromIndex(index, partition):
    comPerm = []
    comIndex = comIndexFromIndex(index, partition)
    for i in range(len(comIndex)):
        comPerm.append(PermFromCode(generatePermCodeFromIndex(comIndex[i], len(partition[i])),partition[i]))
    return comPerm

def generateSolutionFromIndex(index, F):
    partitionCode, comPermIndex = generatePartitionCodeAndPermIndex(F, index)
    partition = generatePartition(partitionCode)
    return comPermFromIndex(comPermIndex, partition)

"____________________________________________________________________________________________________________________________"

"the following are the functions involved with generating costs for specific solutions and parameters"

from numpy import zeros

def constructRouteMatrix(soln, L, X):
    size = len(X) + 1
    N = zeros((size, size))
    for perm in soln:
        leftovers = L
        returnHome = 1
        for i in range(len(perm)-1):
            P = X[perm[i]-1]
            if returnHome == 1:
                N[0][perm[i]] += 1
            if leftovers > P:
                leftovers -= P
                restocks = 0
                returnHome = 0
            else:
                P -= leftovers
                if P%L == 0:
                    restocks = P//L
                    returnHome = 1
                    leftovers = L
                else:
                    restocks = P//L + 1
                    returnHome = 0
                    leftovers = L - P%L
            N[0][perm[i]] += restocks
            N[perm[i]][0] += restocks
            if returnHome == 1:
                N[perm[i]][0] += 1
            else:
                N[perm[i]][perm[i+1]] += 1
        P = X[perm[-1]-1]
        if returnHome == 1:
            N[0][perm[-1]] += 1
        if leftovers > P:
            restocks = 0
        else:
            P -= leftovers
            restocks = (P-1)//L + 1
        N[0][perm[-1]] += restocks
        N[perm[-1]][0] += restocks + 1
    return N

def cost(N, C):
    itterations = range(len(C))
    cost = 0
    for i in itterations:
        for j in itterations:
            cost += N[i][j] * C[i][j]
    return cost

"_______________________________________________________________________________________________________________________________________________________________"

"this function returns a vector with all solution qualities, given the relevant paramaters, L = vehicle capacity, X = package vector, C = cost matrix and F = network size"
def constructQualityVector(F, L, X, C):
    q = []
    for index in range(maxIndex(F) + 1):
        q.append(cost(constructRouteMatrix(generateSolutionFromIndex(index, F), L, X) , C))
    return q

"this function returns a solution quality given a single index and the relevant parameters"
def solutionQualityByIndex(F, L, X, C, index):
    quality = cost(constructRouteMatrix(generateSolutionFromIndex(index, F), L, X) , C)
    return quality

"example problem below"
"the conclusion of testing/timing is that for full costing: constructing the full solution space is significantly faster than constructing by index"

##def main():
##    F = 3
##    C = [[0,5,6,7],[5,0,2,3],[6,2,0,1],[7,3,1,0]]
##    L = 20
##    X = [17,15,28]
##    q = constructQualityVector(F, L, X, C)
##    print(q)
##
import time
##
##def main():
##    F = 6
##    C = [[0,18,18,15,13,16,17],[18,0,3,2,3,10,8],[18,3,0,6,6,11,11],[15,2,6,0,15,15,8],[13,3,6,15,0,7,5],[16,10,11,15,7,0,14],[17,8,11,8,5,14,0]]
##    X = [18,24,6,14,23,15]
##    L = 20
##    start = time.time()
##    q = constructQualityVector(F, L, X, C)
##    end = time.time()
##    print(end - start)
##
##
def main():
    F = 6
    C = [[0,18,18,15,13,16,17],[18,0,3,2,3,10,8],[18,3,0,6,6,11,11],[15,2,6,0,15,15,8],[13,3,6,15,0,7,5],[16,10,11,15,7,0,14],[17,8,11,8,5,14,0]]
    X = [18,24,6,14,23,15]
    L = 20
    index = 1000
    start = time.time()
    quality = solutionQualityByIndex(F, L, X, C, index)
    end = time.time()
    print(end - start)
    print(quality)
    
main()