"Note: the partitions are built from the simplest case, the single partition of the set containing just element 1."
"each itteration involves adding the next element one by one to each of the sets contained within each partition, as well as to a set of it's own."
"I couldn't work out the recursive function, but the following achieves the same result (perhaps less efficiently though)"

def expandPartitionList(inputPartitionList, newterm):
    newPartitionList = []
    for partition in inputPartitionList:
        for i in range(len(partition)):
            newpartition = []
            for j in range(len(partition)):
                if i == j: newpartition.append(partition[j] + [newterm])
                else: newpartition.append(partition[j])
            newPartitionList.append(newpartition)
        newPartitionList.append(partition + [[newterm]])
    return newPartitionList

def listOfPartitions(numberOfElements):
    partitionList = [[[1]]]
    for i in range(2,numberOfElements+1): partitionList = expandPartitionList(partitionList, i)
    return partitionList

from itertools import permutations, product  


"this function takes each set within a partition and expands it into its possible permutations"
"this fullList represents the full space of non-degenerate solutions"
def fullList(partitionList):
    fullList = []
    for partition in partitionList:
        permutationListNested = []
        for set in partition:
            permutationListNested.append(list(permutations(set)))
        fullList += list(product(*permutationListNested))
    return fullList
    
def solutionSpace(F): return fullList(listOfPartitions(F))

#for i in range(1,10):
#   print(len(solutionSpace(i)))

"memory error at F = 10, at F = 9 we have a solution space of 4.6 million this growth is faster than factorial"