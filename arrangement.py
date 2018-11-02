#
# Arrangement
#
import numpy as np
from itertools import permutations, combinations
import operator

def calculateExpectedStatisfaction(passengers):
    result = 0;
    for row in passengers:
        for passenger in row:
            if 'W' in passenger:
                result += 1
        if len(row)  > 1:
            result += len(row) * 2 - 2
        else:
            result += 1
    return result


def dict_of_neighbors(passengers):
    result = {}
    for group in passengers:
        for item in group:
            result.update({ item: [x for x in group if x != item] })
    return result


def calculateStatisfactionMatrix(combs, neighbors_by_passengers, seats):
    # Init matrix of statisfaction
    satisfaction_matrix = np.zeros( (len(combs), seats) )

    for row_number, row in enumerate(combs):
        for seat_in_row, passenger in enumerate(row):
            satisfaction = 0
            if 'W' in passenger and ( seat_in_row == 0 or seat_in_row == len(row) - 1 ):
                satisfaction += 1

            if seat_in_row - 1 >= 0:
                neighbor_left = row[seat_in_row - 1]
            else:
                neighbor_left = 'null'

            if seat_in_row + 1 < len(row):
                neighbor_right = row[seat_in_row + 1]
            else:
                neighbor_right = 'null'

            neighbors = neighbors_by_passengers[passenger]
            if(len(neighbors) > 0):
                if neighbor_left in neighbors:
                    satisfaction += 1
                if neighbor_right in neighbors:
                    satisfaction += 1
            else:
                satisfaction += 1
            satisfaction_matrix[row_number][seat_in_row] = satisfaction
    return satisfaction_matrix


def sumStatisfactionByRows(satisfaction_matrix):
    result = {}
    for i, row in enumerate(satisfaction_matrix):
        result.update( {i: sum(row) } )
    result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    return result


# Select right seats
# When we select right rows of arrangements
# we have to remove all of combinations with current passenger
def optimalArrangements(satisfaction_rows, combs):
    result = []
    for item in satisfaction_rows:
        row = combs[item[0]]
        if len(row) == 0:
            continue
        result.append(row)
        for passenger in row:
            for i, row_comb in enumerate(combs):
                if passenger in row_comb:
                    combs[i] = []
    return result
