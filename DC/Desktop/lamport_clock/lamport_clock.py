class LamportClock:
    def __init__(self):
        self.time = 0

    def increment(self):
        """Increment the logical clock."""
        self.time += 1

    def update(self, received_time):
        """Update the clock based on a received timestamp."""
        self.time = max(self.time, received_time) + 1

    def get_time(self):
        """Get the current logical time."""
        return self.time

    def __str__(self):
        return f"LamportClock(time={self.time})"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Example usage with two processes
    clock1 = LamportClock()
    clock2 = LamportClock()

    print("Initial clocks:")
    print(f"Process 1: {clock1}")
    print(f"Process 2: {clock2}")

    # Process 1 has an event
    clock1.increment()
    print(f"\nProcess 1 increments: {clock1}")

    # Process 1 sends a message to Process 2
    message_time = clock1.get_time()
    print(f"Process 1 sends message with time: {message_time}")

    # Process 2 receives the message and updates its clock
    clock2.update(message_time)
    print(f"Process 2 updates after receiving message: {clock2}")

    # Process 2 has a local event
    clock2.increment()
    print(f"Process 2 increments: {clock2}")

    # Process 1 has another event
    clock1.increment()
    print(f"Process 1 increments again: {clock1}")
