from itertools import permutations, product

from numpy import zeros

from math import factorial

from collections import Counter

from resupply import solutionSpace, constructQualityVector

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