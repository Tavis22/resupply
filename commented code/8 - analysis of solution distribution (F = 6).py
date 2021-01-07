"the following functions are taken from the '1-creating solution space'"
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

def fullList(partitionList):
    fullList = []
    for partition in partitionList:
        permutationListNested = []
        for set in partition:
            permutationListNested.append(list(permutations(set)))
        fullList += list(product(*permutationListNested))
    return fullList
    
def solutionSpace(F): return fullList(listOfPartitions(F))

"_______________________________________________________________________________________________________________"

"for each solution, we'll have to construct a Route matrix, N, which contains the number of routes taken between nodes"
from numpy import zeros

"This function generates the Route Matrix for a particular solution (soln), vehicle capacity (L), package vector (X)"
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

"this function determines the cost for a given Route Matrix and Cost Matrix"
def cost(N, C):
    itterations = range(len(C))
    cost = 0
    for i in itterations:
        for j in itterations:
            cost += N[i][j] * C[i][j]
    return cost

"this function returns a vector with all solution qualities, given a solution space and the relevant paramaters, L = vehicle capacity, X = package vector, C = cost matrix"
def constructQualityVector(solutionSpace, L, X, C):
    q = []
    for soln in solutionSpace:
        q.append(cost(constructRouteMatrix(soln, L, X) , C))
    return q

"this function returns the solution quality for a single solution"
def solutionQualityByIndex(index, F, L, X, C):
    quality = cost(constructRouteMatrix(solutionSpace(F)[index], L, X) , C)
    return quality

"___________________________________________________________________________________________________________________________________________"


from collections import Counter


"the following is an analysis of a 6 node problem, with randomly generated numbers/parameters."
"the vehicle capacity is varied, where it is clear that different values generate very different quality distributions"
"Note that the lower values actually indicate higher quality solutions"
"also note that at large L, the problem reduces to a typical travelling salesman problem"
def main():
    F = 6
    C = [[0,18,18,15,13,16,17],[18,0,3,2,3,10,8],[18,3,0,6,6,11,11],[15,2,6,0,15,15,8],[13,3,6,15,0,7,5],[16,10,11,15,7,0,14],[17,8,11,8,5,14,0]]
    X = [18,24,6,14,23,15]
    capacities = [5,10,15,20,25,30,35,40,100,1000]
    solutions = solutionSpace(F)
    for L in capacities:
        print("Capacity = ", L)
        q = constructQualityVector(solutions, L, X, C)
        tally = Counter(q)
        orderedKeys = sorted(tally)
        print("Distribution of costs for the ", len(q), " solutions")
        for i in orderedKeys:
            print(int(i),':', tally[i])
        bestQuality = orderedKeys[0]
        bestSolutionIndex = [i for i,x in enumerate(q) if x==bestQuality]
        print("The best quality solution(s) are:")
        for i in bestSolutionIndex:
            print(solutions[i])
        print("\n")
        
main()