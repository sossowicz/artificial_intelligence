import sys
import pandas as pd
import numpy as np

class Node:
    def __init__(self, data = None, value = None, point = None, right = None, left = None):
        self.data = data # axis along node splits data
        self.value = value # value at splitting axis
        self.point = point # data point at this node
        self.right = right # reference to right child
        self.left = left # reference to left child

def BuildKdTree(P, D): # Set of points P of M dimensions and current depth D
    M = P.shape[1] # M dimensions
    if len(P) == 0: # If P is empty then return none
        return None 
    elif len(P) == 1: # If P has only one data point
        node = Node(data = D%M, value = P.iloc[0, D%M], point = P.iloc[0])
        return node
    else:
        data = D%M
        value = np.median(P.iloc[:, data])
        elementDifference = np.abs(P.iloc[:, data] - value)
        indexMedian = (P.iloc[:, data] - value).abs().idxmin()
        node = Node(data = data, value = value, point = P.loc[indexMedian])
        # points in P for which value at dimension d is less than or equal to val, D+1
        subLeft = P[P.iloc[:, data] <= value]
        # ensure no median value 
        subLeft = subLeft.drop(indexMedian, errors = 'ignore')
        # build KdTree
        node.left = BuildKdTree(subLeft, D+1)
        # points in P for which value at dimension d is greater than val, D+1
        subRight = P[P.iloc[:, data] > value]
        # ensure no median value 
        subRight = subRight.drop(indexMedian, errors = 'ignore')
        # build KdTree
        node.right = BuildKdTree(subRight, D+1)
        return node


def KdTreeSearch(root, query):
    # base case at empty subtree without finding better match
    if root is None:
        return 1e10, None

    # calculate number of dimensions
    M = len(root.point)
    axis = root.data

    # which brance of current root node to explore first
    if (query[axis] >= root.value):
        nextBranch = root.right
        oppBranch = root.left
    else:
        nextBranch = root.left
        oppBranch = root.right

    # squared euclidean distance between query and current root node
    elementDiff = root.point[:-1] - query
    rootDistance = np.sum(np.square(elementDiff))
    # call using recursion
    bestDistance, bestPoint = KdTreeSearch(nextBranch, query)

    # update best point and distance if needed
    if rootDistance < bestDistance:
        bestPoint = root.point
        bestDistance = rootDistance

    # update """"""
    if (query[axis] - root.value)**2 < bestDistance:
        # search opposite branch
        newDistance, newPoint = KdTreeSearch(oppBranch, query)
        if newDistance < bestDistance:
            bestPoint = newPoint
            bestDistance = newDistance

    return bestDistance, bestPoint



def main():
    def read(file):
        return pd.read_csv(file, sep="\s+", header=None)
    
    def clean(data):
        data = data.apply(pd.to_numeric, errors='coerce')
        return data.dropna()
    
    trainFile = sys.argv[1]
    trainData = read(trainFile)
    trainData = clean(trainData)

    testFile = sys.argv[2]
    testData = read(testFile)
    testData = clean(testData)

    dimension = sys.argv[3]

    tree = BuildKdTree(trainData, 0)

    nn = []
    for _, row in testData.iterrows():
        search = KdTreeSearch(tree, row)
        nearestNeighbour = search[1]
        last = nearestNeighbour.iloc[-1]
        lastInt = int(last)
        nn.append(lastInt)

    for n in nn:
        print(n)

if __name__ == "__main__":
    main()