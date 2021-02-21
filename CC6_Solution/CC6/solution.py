"""
Solution
Coding Challenge 6
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from queue import SimpleQueue


def gates_needed(departures, arrivals):
    """
    Finds the maximum number of airport gates needed for the given day
    param departures: depart times of airplanes
    param arrivals: arrival times of airplanes
    return: the max number of gates needed
    """
    if not departures:
        return len(arrivals)
    maximum = 0
    depart_queue = SimpleQueue()
    arrive_queue = SimpleQueue()
    for time in departures:
        depart_queue.put(time)
    for time in arrivals:
        arrive_queue.put(time)

    current_gates = 0
    new_depart = True
    new_arrive = True

    while (not arrive_queue.empty()) and (not depart_queue.empty() or not new_depart):
        if new_depart:
            current_departure = depart_queue.get()
        if new_arrive:
            current_arrival = arrive_queue.get()

        if current_arrival < current_departure:
            current_gates += 1
            if current_gates > maximum:
                maximum = current_gates
            new_arrive = True
            new_depart = False
        elif current_arrival > current_departure:
            current_gates -= 1
            new_arrive = False
            new_depart = True
        else:
            new_depart = True
            new_arrive = True

    if not arrive_queue.empty():
        if not (new_arrive and new_depart):
            current_gates += 1
        while not arrive_queue.empty():
            arrive_queue.get()
            current_gates += 1

    if current_gates > maximum:
        maximum = current_gates
    return maximum

'''
def main():
    departures = [num for num in range(25)]
    arrivals = [num for num in range(26)]
    print(gates_needed(departures, arrivals))

main()
'''