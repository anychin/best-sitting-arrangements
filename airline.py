import sys
import numpy as np
from arrangement import *

seats = 0
rows = 0
passengers = []
expected_satisfaction = 0
real_satisfaction = 0



def init(file):
    with open(file) as fp:
        for i, line in enumerate(fp):
            data = line.split()
            if i == 0:
                seats = int(data[0])
                rows = int(data[1])
            else:
                passengers.append(data)
    return [seats, rows, passengers]


# Run script
seats, rows, passengers = init(sys.argv[1])

# Create List of passengers
separated_passengers = [item for sublist in passengers for item in sublist]

if len(separated_passengers) > seats * rows:
    print("Too much passengers, sorry")
    exit()

# Unique Combinations (Permutations) of seats arrangements
all_seating_arrangements = list(permutations(separated_passengers, seats))

# Creaate Dictionary of neighbors
neighbors_by_passengers = dict_of_neighbors(passengers)

# Calculate values of statisfaction passengers by all
# combinations of arrangements
# Example:
# [ [2 0 1 0],
#   [2 1 1 2],
#   [2 1 1 0] ]
satisfaction_matrix = calculateStatisfactionMatrix(
                            all_seating_arrangements,
                            neighbors_by_passengers,
                            seats )

satisfaction_rows = sumStatisfactionByRows(satisfaction_matrix)

arrangements = optimalArrangements(satisfaction_rows, all_seating_arrangements)

expected_satisfaction = calculateExpectedStatisfaction(passengers)
real_satisfaction_matrix = calculateStatisfactionMatrix(arrangements, neighbors_by_passengers, seats)
satisfaction = np.sum(real_satisfaction_matrix) * 100 / expected_satisfaction


print('\nGroups of Passengers:')
for row in passengers:
    print(' '.join(row))

print('\nBest arrangements:')
for row in arrangements:
    print(' '.join(row))

print('\nSatisfaction:')
print('{0} %'.format(satisfaction))
print('\n')
