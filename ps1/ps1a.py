###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    f = open(filename)
    cow_dict = {}
    for line in f:
        name, weight = line.split(",")
        cow_dict[name] = int(weight.replace("/n",""))
    f.close()
    return cow_dict


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = cows.copy()
    trip_list = []
    while cows_copy != {}:
        trip = []
        weight = 0
        while weight + min(cows_copy.values(),default = 0) <= limit and cows_copy != {}:
            slim_cows = {}
            for cow in cows_copy:
                if cows_copy[cow] <= (limit-weight):
                    slim_cows[cow] = cows_copy[cow]
            if slim_cows != {}:
                goodcow, goodweight = max(slim_cows, key =slim_cows.get), max(slim_cows.values())
                weight += goodweight
                cows_copy.pop(goodcow)
                trip.append(goodcow)
        trip_list.append(trip)
    return trip_list

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy=cows.copy()
    trip_schedule_lists= []
    cow_names = cows_copy.keys()
    for trip_schedule in get_partitions(cow_names):
        valid_trip = True
        for trip in trip_schedule:
            weight = 0
            for cow in trip:
                weight += cows[cow]
            if weight > limit:
                valid_trip = False
        if valid_trip == True:
            trip_schedule_lists.append(trip_schedule)
    best_list = min(trip_schedule_lists, key = len)
    return best_list

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    file = "ps1_cow_data.txt"
    print("Number of trips using greedy algorithm:")
    start_greedy = time.time()
    print(len(greedy_cow_transport(load_cows(file))))
    end_greedy = time.time()
    greedy_time = end_greedy - start_greedy
    print(f"Time taken for greedy algrorithm to run is {greedy_time}")
    print("Number of trips using brute force algorithm:")
    start_brute = time.time()
    print(len(brute_force_cow_transport(load_cows(file))))
    end_brute = time.time()
    brute_time = end_brute - start_brute
    print(f"Time taken for brute force algrorithm to run is {brute_time}")

compare_cow_transport_algorithms()
