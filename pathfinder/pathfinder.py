import sys
import math
from heapq import heappop, heappush

class Problem:
    def __init__(self, map_data, start, end):
        self.map_data = map_data
        self.start = start
        self.end = end
    #possible next moves
    def expand(self, state):
        x, y = state
        order = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            #print("move : ", move)
            movex, movey = move
            newx, newy = x+movex, y+movey
            if newx<0 or newx>=len(self.map_data) or newy<0 or newy>=len(self.map_data[0]) or self.map_data[newx][newy]==-1:
                continue
            order.append((newx, newy))
        return order

    #for astar
    def heuristic(self, state, heuristic):
        if heuristic == "manhattan":
            return abs(state[0]-self.end[0]) + abs(state[1]-self.end[1]-10)
        elif heuristic == "euclidean":
            return math.sqrt((state[0]-self.end[0])**2 + (state[1]-self.end[1])**2)
    #cost
    def path_cost(self, cost, state, nextState):
        return cost + abs((self.map_data[nextState[0]][nextState[1]]) - (self.map_data[state[0]][state[1]])) + 1

def bfs(problem):
    fringe = [(problem.start, [])]
    visited = set()
    while fringe:
        state, path = fringe.pop(0)
        if state == problem.end:
            return path
        if state not in visited:
            visited.add(state)
            for new_state in problem.expand(state):
                new_path = path + [state]
                fringe.append((new_state, new_path))
    return path


def ucs(problem):
    fringe = [(0, problem.start, [])]
    visited = set()
    while fringe:
        cost, state, path = fringe.pop(0)
        #print('Path, ', path)
        if state == problem.end:
            return path, cost
        if state not in visited:
            visited.add(state)
            for new_state in problem.expand(state):
                new_path = path + [new_state]
                new_cost = problem.path_cost(cost, state, new_state) 
                fringe.append((new_cost, new_state, new_path))
            fringe.sort(key=lambda x: x[0])
    return None

def astar(problem, heuristic):
    fringe = [(problem.heuristic(problem.start, heuristic), problem.start, [])]
    visited = set()
    while fringe:
        cost, state, path = fringe.pop(0)
        if state == problem.end:
            return path, cost
        if state not in visited:
            visited.add(state)
            for new_state in problem.expand(state):
                new_path = path + [new_state]
                new_cost = problem.path_cost(cost, state, new_state)
                estimate = new_cost + problem.heuristic(new_state, heuristic) #f(n)
                fringe.append((estimate, new_state, new_path))
            fringe.sort(key=lambda x: x[0])
    return None

def main():
    map_file_path = sys.argv[1]
    algorithm = sys.argv[2]
    if len(sys.argv) == 3:
        heuristic = None
    else:
        heuristic = sys.argv[3]

    with open(map_file_path) as mapLoad:
        rows, cols = map(int, mapLoad.readline().strip().split())

        start = [int(val) for val in mapLoad.readline().strip().split()]
        start = tuple(start)
        start = (start[0] - 1, start[1] - 1)

        end = [int(val) for val in mapLoad.readline().strip().split()]
        end = tuple(end)
        end = (end[0] - 1, end[1] - 1)

        map_data = []
        for i in range(rows):
            row = mapLoad.readline().strip().split()
            rowVal = []
            for val in row:
                if val != "X":
                    rowVal.append(int(val))
                else:
                    rowVal.append(-1)
            map_data.append(rowVal)

    problem = Problem(map_data, start, end)



    if algorithm == "bfs":
        result = bfs(problem)
        if result is None:
            print("null")
            return
        path = result
    elif algorithm == "ucs":
        result = ucs(problem)
        if result is None:
            print("null")
            return
        path, cost = result
    elif algorithm == "astar":
        result = astar(problem, heuristic)
        if result is None:
            print("null")
            return
        path, cost = result
    else:
        return

    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if (i, j) == start or (i, j) == end or (i, j) in path:
                print("*", end=" ")
            elif map_data[i][j] == -1:
                print("X", end=" ")
            else:
                print(map_data[i][j], end=" ")
        print()

if __name__ == "__main__":
    main()
           
