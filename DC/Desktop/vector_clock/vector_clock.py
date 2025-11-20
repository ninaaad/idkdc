import copy

class VectorClock:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.clock = [0] * num_processes

    def increment(self):
        """Increment the clock for this process."""
        self.clock[self.process_id] += 1

    def update(self, other_clock):
        """Update this clock with the maximum values from another clock."""
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], other_clock[i])

    def merge(self, other_clock):
        """Merge two vector clocks by taking the maximum of each component."""
        merged = copy.deepcopy(self)
        merged.update(other_clock)
        return merged

    def compare(self, other_clock):
        """Compare two vector clocks.
        Returns:
        -1 if self < other (self happened before other)
         0 if self == other (concurrent)
         1 if self > other (self happened after other)
        """
        less = False
        greater = False
        for i in range(len(self.clock)):
            if self.clock[i] < other_clock[i]:
                less = True
            elif self.clock[i] > other_clock[i]:
                greater = True
        if less and not greater:
            return -1
        elif greater and not less:
            return 1
        else:
            return 0

    def __str__(self):
        return f"VectorClock({self.clock})"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Example usage with 3 processes
    vc1 = VectorClock(0, 3)
    vc2 = VectorClock(1, 3)
    vc3 = VectorClock(2, 3)

    print("Initial clocks:")
    print(f"Process 1: {vc1}")
    print(f"Process 2: {vc2}")
    print(f"Process 3: {vc3}")

    # Process 1 sends a message to Process 2
    vc1.increment()
    print(f"\nProcess 1 increments: {vc1}")

    # Process 2 receives the message and updates its clock
    vc2.update(vc1.clock)
    vc2.increment()
    print(f"Process 2 updates and increments: {vc2}")

    # Process 3 has a local event
    vc3.increment()
    print(f"Process 3 increments: {vc3}")

    # Compare clocks
    print(f"\nComparison vc1 vs vc2: {vc1.compare(vc2.clock)}")
    print(f"Comparison vc2 vs vc3: {vc2.compare(vc3.clock)}")
    print(f"Comparison vc1 vs vc3: {vc1.compare(vc3.clock)}")
