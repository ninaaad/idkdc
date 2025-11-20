import socket
import threading
import time
import struct

class Master:
    def __init__(self, host='localhost', port=12346, num_slaves=3):
        self.host = host
        self.port = port
        self.num_slaves = num_slaves
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.slave_times = {}
        self.slave_sockets = {}
        print(f"Master listening on {self.host}:{self.port}")

    def handle_slave(self, slave_socket, addr):
        slave_id = addr[1]  # Use port as ID for simplicity
        self.slave_sockets[slave_id] = slave_socket
        print(f"Slave {slave_id} connected from {addr}")

        # Wait for synchronization request
        while True:
            try:
                # Receive slave's time
                data = slave_socket.recv(8)
                if not data:
                    break
                slave_time = struct.unpack('d', data)[0]
                self.slave_times[slave_id] = slave_time
                print(f"Received time from slave {slave_id}: {slave_time}")

                # Send acknowledgment (could be offset later)
                # For now, just ack
                slave_socket.sendall(struct.pack('d', 0.0))  # Placeholder

            except Exception as e:
                print(f"Error with slave {slave_id}: {e}")
                break
        slave_socket.close()
        del self.slave_sockets[slave_id]
        del self.slave_times[slave_id]

    def synchronize_clocks(self):
        # Collect own time
        master_time = time.time()
        print(f"Master time: {master_time}")

        # Wait for all slaves to connect and send times
        while len(self.slave_times) < self.num_slaves:
            time.sleep(0.1)

        # Compute average time
        all_times = list(self.slave_times.values()) + [master_time]
        average_time = sum(all_times) / len(all_times)
        print(f"Average time: {average_time}")

        # Compute offsets for slaves
        for slave_id, slave_time in self.slave_times.items():
            offset = average_time - slave_time
            print(f"Offset for slave {slave_id}: {offset}")
            # Send offset to slave
            if slave_id in self.slave_sockets:
                self.slave_sockets[slave_id].sendall(struct.pack('d', offset))

        # Master adjusts its own clock (in simulation)
        master_offset = average_time - master_time
        print(f"Master offset: {master_offset}")

    def run(self):
        # Start accepting slaves
        for _ in range(self.num_slaves):
            slave_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_slave, args=(slave_socket, addr)).start()

        # After all connected, synchronize
        time.sleep(1)  # Wait for threads to start
        self.synchronize_clocks()

class Slave:
    def __init__(self, host='localhost', port=12346, slave_id=1):
        self.host = host
        self.port = port
        self.slave_id = slave_id
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.offset = 0.0

    def synchronize(self):
        try:
            self.client_socket.connect((self.host, self.port))

            # Send current time
            current_time = time.time()
            self.client_socket.sendall(struct.pack('d', current_time))
            print(f"Slave {self.slave_id} sent time: {current_time}")

            # Receive offset
            data = self.client_socket.recv(8)
            self.offset = struct.unpack('d', data)[0]
            print(f"Slave {self.slave_id} received offset: {self.offset}")

            # Adjust clock (in simulation)
            adjusted_time = current_time + self.offset
            print(f"Slave {self.slave_id} adjusted time: {adjusted_time}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

def run_master():
    master = Master()
    master.run()

def run_slave(slave_id):
    slave = Slave(slave_id=slave_id)
    slave.synchronize()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'master':
        run_master()
    elif len(sys.argv) > 2 and sys.argv[1] == 'slave':
        slave_id = int(sys.argv[2])
        run_slave(slave_id)
    else:
        print("Usage: python berkeley_algorithm.py master  # to run master")
        print("       python berkeley_algorithm.py slave <id>  # to run slave with id")
