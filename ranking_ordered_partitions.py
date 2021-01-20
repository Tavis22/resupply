"""this code ranks ordered partitions
Note that it is assumed these ordered partitions are sorted, i.e. the group containing the first element comes first, and so on."""

"""returns the number of elements in a solution"""
def get_N(soln):
    count = 0
    for group in soln:
        count += len(group)
    return count

"""returns the number of groups in a solution"""
def get_K(soln):
    return len(soln)

"""returns the Lah number for a given n and k. that is, the number of ordered partitions of n elements with k groups"""
def Lah(n,k):
    if n == k: return 1
    if k > n: return 0
    if n == 0 or k == 0: return 0
    return Lah(n-1, k-1) + (n+k-1)*Lah(n-1, k)

"""returns the number of solutions in the N solution space"""
def total_soln(N):
    count = 0
    for k in range(1,N+1):
        count += Lah(N,k)
    return count

"""returns the index of a solution within the total solution space. the deepcopy is included because the get_partial_index function is destructive"""
import copy
def get_index(soln):
    N = get_N(soln)
    K = get_K(soln)
    count = 0
    soln_copy = copy.deepcopy(soln)
    for k in range(1,K):
        count += Lah(N,k)
    return count + get_partial_index(soln_copy)

"""returns the max element present in a solution"""
def max_element(soln):
    return max([max(group) for group in soln])

"""returns the group number within which the max element is located"""
def x_group_location(soln, x):
    for i in range(len(soln)):
        if x in soln[i]: return i

"""returns the location in which the max element has been inserted"""
def x_insert_location(soln, x, location):
    count = 0
    for i in range(location):
        count += len(soln[i]) + 1
    count += soln[location].index(x)
    return count

"""returns the index of a soln within the specific space of solutions with K groups
note that any solution entered into this function will be destroyed"""
def get_partial_index(soln):
    x = max_element(soln)
    if x == 1: return 0
    location = x_group_location(soln, x)
    if len(soln[location]) == 1:
        del soln[location]
        return get_partial_index(soln)
    else:
        N = get_N(soln)
        K = get_K(soln)
        position = x_insert_location(soln, x, location)
        soln[location].remove(x)
        return position + (N+K-1)*get_partial_index(soln) + Lah(N-1, K-1)


"""the following is for the purpose of un-indexing any arbitrary index to create its unique solution"""

"""this function determines from the index and N, the number of groups, K, which the solution has.
It also returns the index of the solution within the (N,K) solution space"""
def k_and_subindex_from_index(index, N):
    for k in range(1, N+1):
        count = Lah(N,k)
        if index < count: return k, index
        else: index -= count
    print('index is too large, max index for given N is: ', total_soln(N) - 1)

"""this function takes the index of a solution within the (N,K) solution space and returns its unique signature"""
def signature(K, subindex, N):
    signature = {}
    for x in range(N,1,-1):
        count = Lah(N-1, K-1)
        if subindex < count:
            signature[x] = 'alone'
            N -= 1
            K -= 1
        else:
            subindex -= count
            position = subindex % (N+K-1)
            subindex //= (N+K-1)
            signature[x] = position
            N -= 1
    return signature
            
"""this function creates a solution from it's unique signature"""
def solution_from_signature(signature):
    soln = [[1]]
    for i in range(2, 2+len(signature)):
        if signature[i] == 'alone': soln.append([i])
        else:
            position = signature[i]
            for j in range(len(soln)):
                if position <= len(soln[j]):
                    soln[j] = soln[j][:position] + [i] + soln[j][position:]
                    break
                else:
                    position -= len(soln[j]) + 1
    return soln

"""bringing it all together"""
def soln_from_index(N, index):
    K, subindex = k_and_subindex_from_index(index, N)
    return solution_from_signature(signature(K, subindex, N))

"""testing below"""
# N = 4
# indices = [i for i in range(total_soln(N))]
# solutions = [soln_from_index(N, index) for index in indices]
# indices_again = [get_index(soln) for soln in solutions]
# print(indices == indices_again)