# Task 1 answer.
def task1():
    # List of speed readings.
    speeds = [20, 25, 60, 50, 55, 90, 95]
    # Counter to track speed increases.
    count = 0

    # Loop through speeds, from second item.
    for i in range(1, len(speeds)):
        # Checking if current speed is more than 30 units higher than the previous.
        if speeds[i] - speeds[i - 1] > 30:
            # Increment counter if the condition is met.
            count += 1

    # Store final count as the result
    result = count
    return result

# Task 2 answer.
def task2():
    # Separate lists of speeds and timestamps.
    speeds = [20, 25, 60, 50, 55, 90, 95]
    timestamps = [0, 1, 2, 3, 4, 5, 6]

    # To track longest duration of speed increases.
    max_duration = 0
    # Start index of a potential increasing sequence.
    start = 0

    # Loop through the speeds, from second item.
    for i in range(1, len(speeds)):
        if speeds[i] > speeds[i - 1]:
            # If speed is increasing, calculate duration from start to current item.
            duration = timestamps[i] - timestamps[start]
            # Update max_duration if current duration is longer.
            max_duration = max(max_duration, duration)

    else:
        # If speed does not increase, reset the start of the increasing sequence.
        start = i

    # Store the longest duration found as the result.
    result = max_duration
    return result

if __name__ == "__main__":
    print(f"Task 1 answer: {task1()}")
    print(f"Task 2 answer: {task2()}")
    