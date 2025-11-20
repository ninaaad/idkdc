import socket
import threading
import time
import struct

class TimeServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Time server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, addr):
        print(f"Connected to {addr}")
        while True:
            try:
                # Receive client's request with T0
                data = client_socket.recv(8)
                if not data:
                    break
                T0 = struct.unpack('d', data)[0]
                print(f"Received T0: {T0}")

                # Server time when request received
                T1 = time.time()
                print(f"Server T1: {T1}")

                # Simulate processing time (optional)
                time.sleep(0.01)  # 10ms delay

                # Server time when sending response
                T2 = time.time()
                print(f"Server T2: {T2}")

                # Send T1 and T2 back
                response = struct.pack('dd', T1, T2)
                client_socket.sendall(response)

            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

class TimeClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def synchronize(self):
        try:
            self.client_socket.connect((self.host, self.port))

            # Send T0
            T0 = time.time()
            self.client_socket.sendall(struct.pack('d', T0))
            print(f"Sent T0: {T0}")

            # Receive T1 and T2
            data = self.client_socket.recv(16)
            T1, T2 = struct.unpack('dd', data)
            print(f"Received T1: {T1}, T2: {T2}")

            # Client time when response received
            T3 = time.time()
            print(f"Client T3: {T3}")

            # Calculate RTT
            RTT = T3 - T0
            print(f"RTT: {RTT}")

            # Estimated server time
            estimated_server_time = T1 + (RTT / 2)
            print(f"Estimated server time: {estimated_server_time}")

            # Adjust client clock (in simulation, just print the adjustment)
            adjustment = estimated_server_time - T3
            print(f"Clock adjustment needed: {adjustment} seconds")

            # In a real system, you would set the system clock here
            # For demonstration, we'll just print

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

def run_server():
    server = TimeServer()
    server.run()

def run_client():
    client = TimeClient()
    client.synchronize()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        run_server()
    elif len(sys.argv) > 1 and sys.argv[1] == 'client':
        run_client()
    else:
        print("Usage: python christian_algorithm.py server  # to run server")
        print("       python christian_algorithm.py client  # to run client")
