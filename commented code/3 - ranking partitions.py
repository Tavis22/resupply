"this function returns the number of unique elements in the partition"
def getSize(partition):
    size = 0
    for group in partition:
        size += len(group)
    return size

"this function generates a code for a particular partition - the code for a partition is a list of the branches taken to arrive at that node"
def getCode(partition):
    size = getSize(partition)
    groups = len(partition)
    code = []
    for element in range(2, size + 1):
        for group in range(groups):
            if element in partition[group]:
                code.append(group)
    return code

"this is a recursive function which returns the number of endpoints that exist at the desired depth from any vertex"
def endpoints(code, maxDepth):
    count = 0
    if len(code) == maxDepth: return 1
    branches = max(code) + 2
    for i in range(branches):
        count += endpoints(code + [i], maxDepth)
    return count

"this code returns the index of a partition, it acts by stepping all the way back through the tree/graph, adding the number of endpoints for all nodes below it"
def getIndex(partition):
    code = getCode(partition)
    maxDepth = len(code)
    index = 0
    while len(code) > 0:
        for i in range(code[-1]):
            code[-1] = i
            index += endpoints(code, maxDepth)
        del(code[-1])
    return index
