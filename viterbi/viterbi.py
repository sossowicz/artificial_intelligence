import numpy as np
import sys

#                N        S       W        E
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def make_tm(input_map, filter_obstacles):
    K = len(filter_obstacles)
    tm = np.zeros((K, K))

    for pos, num in filter_obstacles.items():
        good_neighbours = []
        for direction in DIRECTIONS:
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if (neighbor in filter_obstacles):
                good_neighbours.append(neighbor)

        for good_neighbour in good_neighbours:
            tm[num][filter_obstacles[good_neighbour]] = 1/len(good_neighbours)
    return tm

def make_em(sensor_readings, input_map, error_rate, filter_obstacles):
    K = len(filter_obstacles)
    N = len(sensor_readings)
    em = np.zeros((K, N))

    for pos, num in filter_obstacles.items():
        for sensor_reading in sensor_readings:

            sensor = []
            for direction in DIRECTIONS:
                neighbor = (pos[0]+direction[0], pos[1]+direction[1])
                if (neighbor in filter_obstacles):
                    sensor.append('0')
                else:
                    sensor.append('1')

            errors = 0
            for i in range(4):
                if (sensor[i] != sensor_reading[i]):
                    errors += 1

            em[num][sensor_readings.index(sensor_reading)] = (error_rate ** errors)*((1-error_rate)**(4-errors))
    return em


def viterbi(O, S, Pi, Y, Tm, Em):
    K = len(S)
    T = len(Y)
    trellis = np.zeros((K, T))

    # for each position i = 1, 2, ..., K
    for i in range(K):
        trellis[i, 0] = Pi[i]*Em[i, O.index(Y[0])]

    # for each observation j = 2, 3, ...T
    for j in range(1, T):
        # for each state i = 1, 2, ...K
        for i in range(K):
            maximum = -1
            for k in range(K):
                probability = trellis[k, j - 1]*Tm[k, i]*Em[i, O.index(Y[j])]
                if (probability > maximum):
                    maximum = probability
            trellis[i, j] = maximum
    return trellis

def main():
    input_file = sys.argv[1]
    file = open(input_file)

    # Extract rows cols
    rows, cols = map(int, file.readline().split())

    # Extract map
    input_map = np.zeros((rows, cols))
    for i in range(rows):
        row_data = file.readline().split()
        for j in range(cols):
            if (row_data[j] == 'X'):
                input_map[i, j] = 1
            else:
                input_map[i, j] = 0

    # Extract sensor num
    num_sensors = int(file.readline())

    # Extract sensor data
    sensor_readings = []
    for _ in range(num_sensors):
        sensor_readings.append(file.readline().strip())

    # Extract error_rate rate
    error_rate = float(file.readline())

    file.close()

    # Create a table which maps only traversable positions with an index
    num = 0
    filter_obstacles = {}
    for i in range(cols):
        for j in range(rows):
            if (input_map[j, i] == 0):
                filter_obstacles[(j, i)] = num
                num += 1

    # Evaluate probability distribution
    Pi = []
    obstacles = len(filter_obstacles)
    for _ in range(obstacles):
        Pi.append(1/obstacles)

    # run
    Tm = make_tm(input_map, filter_obstacles)
    Em = make_em(sensor_readings, input_map, error_rate, filter_obstacles)
    trellis = viterbi(sensor_readings, np.array(list(filter_obstacles.values())), Pi, sensor_readings, Tm, Em)

    maps = []
    for i in range(num_sensors):
        mapvalue = np.zeros((rows, cols))
        for j in range(rows):
            for k in range(cols):
                if ((j, k) in filter_obstacles):
                    mapvalue[j, k] = trellis[filter_obstacles[(j, k)], i]
                else:
                    mapvalue[j, k] = 0
        maps.append(mapvalue)

    np.savez("output.npz", *maps)

if __name__ == "__main__":
    main()
