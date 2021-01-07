from itertools import permutations, product

from numpy import zeros, savetxt

from math import factorial

from collections import Counter

from resupply import solutionSpace, constructQualityVector

"the following is an analysis of a 3 node problem, with randomly generated numbers/parameters."
"the vehicle capacity is varied, where it is clear that different values generate very different quality distributions"
"Note that the lower values actually indicate higher quality solutions"
"also note that at large L, the problem reduces to a typical travelling salesman problem"
def main():
    F = 8
    C = [[0,10,16,10,14,17,12,11,17],[10,0,7,8,14,9,4,1,5],[16,7,0,15,10,10,5,2,11],[10,8,15,0,5,15,13,15,15],[14,14,10,5,0,1,4,15,4],[17,9,10,15,1,0,13,5,3],[12,4,5,13,4,13,0,2,7],[11,1,2,15,15,5,2,0,2],[17,5,11,15,4,3,7,2,0]]
    X = [23,18,28,7,23,27,9,22]
    capacities = [10,15,20,25,30,35,40,100]
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
        
"choosing L = 20. outputting the quality vector and quality distribution"
def main2():
    F = 8
    C = [[0,10,16,10,14,17,12,11,17],[10,0,7,8,14,9,4,1,5],[16,7,0,15,10,10,5,2,11],[10,8,15,0,5,15,13,15,15],[14,14,10,5,0,1,4,15,4],[17,9,10,15,1,0,13,5,3],[12,4,5,13,4,13,0,2,7],[11,1,2,15,15,5,2,0,2],[17,5,11,15,4,3,7,2,0]]
    X = [23,18,28,7,23,27,9,22]
    L = 20
    solutions = solutionSpace(F)
    q = constructQualityVector(solutions, L, X, C)
    tally = Counter(q)
    orderedKeys = sorted(tally)
    qdist = []
    for i in orderedKeys:
        qdist.append([i,tally[i]])
    savetxt("8nodeQualityVector.csv", q, delimiter=",")
    savetxt("8nodeQualityDistribution.csv", qdist, delimiter=",")

main2()
    