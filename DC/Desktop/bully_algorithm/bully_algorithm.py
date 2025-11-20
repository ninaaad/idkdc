import threading
import time
import random

class Process:
    def __init__(self, process_id, all_processes):
        self.process_id = process_id
        self.all_processes = all_processes
        self.is_alive = True
        self.is_leader = False
        self.election_in_progress = False
        self.leader_id = None

    def start_election(self):
        if self.election_in_progress:
            return
        self.election_in_progress = True
        print(f"Process {self.process_id} starts election.")

        # Send election messages to higher ID processes
        higher_processes = [p for p in self.all_processes if p.process_id > self.process_id and p.is_alive]
        responses = []

        for p in higher_processes:
            response = self.send_election_message(p)
            responses.append(response)

        # If no one responds, become leader
        if not any(responses):
            self.become_leader()
        else:
            # Wait for coordinator message
            time.sleep(1)  # Simulate waiting
            if not self.leader_id:
                print(f"Process {self.process_id} did not receive coordinator message, restarting election.")
                self.start_election()

        self.election_in_progress = False

    def send_election_message(self, target_process):
        print(f"Process {self.process_id} sends election message to Process {target_process.process_id}")
        # Simulate sending message
        if target_process.is_alive:
            target_process.receive_election_message(self)
            return True
        return False

    def receive_election_message(self, sender):
        print(f"Process {self.process_id} receives election message from Process {sender.process_id}")
        if not self.election_in_progress:
            self.start_election()

    def become_leader(self):
        self.is_leader = True
        self.leader_id = self.process_id
        print(f"Process {self.process_id} becomes the leader.")
        # Announce to all lower processes
        lower_processes = [p for p in self.all_processes if p.process_id < self.process_id and p.is_alive]
        for p in lower_processes:
            p.receive_coordinator_message(self)

    def receive_coordinator_message(self, coordinator):
        self.leader_id = coordinator.process_id
        self.is_leader = False
        print(f"Process {self.process_id} acknowledges Process {coordinator.process_id} as leader.")

    def fail(self):
        self.is_alive = False
        self.is_leader = False
        print(f"Process {self.process_id} has failed.")

    def recover(self):
        self.is_alive = True
        print(f"Process {self.process_id} has recovered.")
        self.start_election()

def simulate_bully_algorithm():
    # Create processes with IDs 1 to 5
    processes = [Process(i, []) for i in range(1, 6)]
    for p in processes:
        p.all_processes = processes

    # Initially, Process 5 is the leader
    processes[4].become_leader()

    print("Initial state: Process 5 is leader\n")

    # Simulate failure of Process 5
    time.sleep(1)
    print("Simulating failure of Process 5...")
    processes[4].fail()

    # Process 4 detects failure and starts election
    time.sleep(1)
    processes[3].start_election()

    # Wait for election to complete
    time.sleep(2)

    print(f"\nFinal leader: Process {max(p.process_id for p in processes if p.is_leader)}")

if __name__ == "__main__":
    simulate_bully_algorithm()
