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
    F = 3
    C = [[0,16,19,12],[16,0,12,17],[19,12,0,10],[12,17,10,0]]
    X = [14,24,8]
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
    F = 3
    C = [[0,16,19,12],[16,0,12,17],[19,12,0,10],[12,17,10,0]]
    X = [14,24,8]
    L = 20
    solutions = solutionSpace(F)
    q = constructQualityVector(solutions, L, X, C)
    tally = Counter(q)
    orderedKeys = sorted(tally)
    qdist = []
    for i in orderedKeys:
        qdist.append([i,tally[i]])
    print(q)
    savetxt("3nodeQualityVector.csv", q, delimiter=",")
    savetxt("3nodeQualityDistribution.csv", qdist, delimiter=",")



main2()
    